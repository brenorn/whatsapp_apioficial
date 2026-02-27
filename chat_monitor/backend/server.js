import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import pg from 'pg';
import cors from 'cors';
import dotenv from 'dotenv';
import axios from 'axios';

dotenv.config();

const { Pool } = pg;
const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.get('/api/chats', async (req, res) => {
    try {
        const query = `
            SELECT phone, 
                   max(created_at) as last_msg_at,
                   (SELECT message FROM whatsapp_messages WHERE phone = m.phone ORDER BY created_at DESC LIMIT 1) as last_message,
                   (SELECT sender FROM whatsapp_messages WHERE phone = m.phone ORDER BY created_at DESC LIMIT 1) as last_sender
            FROM whatsapp_messages m
            GROUP BY phone
            ORDER BY last_msg_at DESC
        `;
        const result = await pool.query(query);
        // O "Handoff" é stateful pelo banco DB-First. Se o last_sender for 'me', a IA tá pausada na essência.
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/messages/:phone', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM whatsapp_messages WHERE phone = $1 ORDER BY created_at ASC', [req.params.phone]);
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/send_message', async (req, res) => {
    try {
        const { phone, message } = req.body;
        // Chama o container Python para ele despachar na Oficial Graph API Auth Token dele
        await axios.post('http://127.0.0.1:5005/api/send', { phone, text: message });

        // Broadcast
        io.emit('new_message', { phone, message, sender: 'me', created_at: new Date() });
        res.json({ status: 'success' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

const PORT = 5006;
server.listen(PORT, () => console.log(`🚀 Monitor Backend (DB & Sockets) em http://localhost:${PORT}`));
