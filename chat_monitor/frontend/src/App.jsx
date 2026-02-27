import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import { Search, MessageSquare, Bot, User, Clock, Zap, MoreVertical, ChevronRight, Send } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Usa o valor do Vite Config proxy se em modo dev, senão vai bater na porta 5006 local
const socket = io('http://localhost:5006');
const api = axios.create({ baseURL: 'http://localhost:5006' });

const ChatMonitor = () => {
    const [chats, setChats] = useState([]);
    const [activeChat, setActiveChat] = useState(null);
    const [messages, setMessages] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [draftMessage, setDraftMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        fetchChats();
        socket.on('new_message', (msg) => {
            if (activeChat && (msg.phone === activeChat.phone)) {
                setMessages(prev => [...prev, msg]);
            }
            fetchChats();
        });
        return () => socket.off('new_message');
    }, [activeChat]);

    useEffect(scrollToBottom, [messages]);

    const fetchChats = async () => {
        try {
            const res = await api.get('/api/chats');
            setChats(res.data);
            setLoading(false);
        } catch (err) {
            console.error("Erro ao buscar chats", err);
        }
    };

    const selectChat = async (chat) => {
        setActiveChat(chat);
        try {
            const res = await api.get(`/api/messages/${chat.phone}`);
            setMessages(res.data);
        } catch (err) {
            console.error("Erro ao buscar mensagens", err);
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!draftMessage.trim() || !activeChat) return;
        setDraftMessage('');
        try {
            await api.post('/api/send_message', {
                phone: activeChat.phone,
                message: draftMessage
            });
            // Mensagem irá brotar via Socket.io no 'new_message'
            fetchChats();
        } catch (err) {
            console.error("Erro enviando mensagem manual", err);
        }
    };

    const filteredChats = chats.filter(c =>
        c.phone?.includes(searchTerm) || c.last_message?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="flex h-screen bg-[#0f172a] text-slate-200 font-sans">
            {/* Sidebar */}
            <aside className="w-[380px] border-r border-slate-800 flex flex-col bg-[#1e293b]/50 backdrop-blur-xl">
                <div className="p-6 border-b border-slate-800">
                    <div className="flex items-center justify-between mb-6">
                        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                            MoveMind <span className="text-slate-200">Monitor</span>
                        </h1>
                    </div>

                    <div className="relative group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 group-focus-within:text-blue-400 transition-colors" />
                        <input
                            type="text"
                            placeholder="Buscar contato ou mensagem..."
                            className="w-full bg-[#0f172a]/50 border border-slate-700 rounded-xl py-2.5 pl-10 pr-4 outline-none focus:border-blue-500/50 transition-all text-sm"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto overflow-x-hidden">
                    {loading ? (
                        <div className="p-10 text-center text-slate-500 text-sm">Carregando mentes...</div>
                    ) : filteredChats.map((chat) => {
                        const handoffCru = chat.last_sender === 'me';
                        return (
                            <motion.div
                                initial={{ x: -20, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                key={chat.phone}
                                onClick={() => selectChat(chat)}
                                className={`p-4 mx-2 my-1 rounded-2xl cursor-pointer transition-all flex items-center gap-4 ${activeChat?.phone === chat.phone ? 'bg-blue-600/10 border border-blue-500/20' : 'hover:bg-slate-800/50 border border-transparent'}`}
                            >
                                <div className={`w-12 h-12 rounded-full flex gap-1 items-center justify-center text-lg font-bold ${activeChat?.phone === chat.phone ? 'bg-blue-500 text-white' : 'bg-slate-700 text-slate-400'}`}>
                                    {handoffCru ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5 opacity-60" />}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex justify-between items-baseline mb-1">
                                        <h4 className="font-semibold text-sm truncate">{chat.phone}</h4>
                                    </div>
                                    <p className="text-xs text-slate-500 truncate italic">
                                        {chat.last_message || 'Nova Sessão'}
                                    </p>
                                </div>
                            </motion.div>
                        )
                    })}
                </div>
            </aside>

            {/* Chat Area */}
            <main className="flex-1 flex flex-col relative overflow-hidden bg-gradient-to-b from-[#0f172a] to-[#020617]">
                <AnimatePresence mode="wait">
                    {!activeChat ? (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex-1 flex flex-col items-center justify-center text-slate-600"
                        >
                            <MessageSquare className="w-16 h-16 opacity-20 mb-6" />
                            <p className="text-sm font-medium">Selecione uma conversa ao lado</p>
                        </motion.div>
                    ) : (
                        <motion.div
                            key={activeChat.phone}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex-1 flex flex-col h-full"
                        >
                            <header className="px-8 py-4 bg-[#1e293b]/30 backdrop-blur-md border-b border-slate-800 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-bold border border-blue-500/30">
                                        P
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-slate-200">Paciente {activeChat.phone}</h3>
                                    </div>
                                </div>
                            </header>

                            <div className="flex-1 overflow-y-auto p-10 flex flex-col gap-6">
                                {messages.map((msg, idx) => (
                                    <motion.div
                                        initial={{ opacity: 0, y: 5 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        key={idx}
                                        className={`flex flex-col max-w-[75%] ${msg.sender === 'bot' || msg.sender === 'me' ? 'self-end' : 'self-start'}`}
                                    >
                                        <div className={`p-4 rounded-2xl text-sm leading-relaxed shadow-lg ${msg.sender === 'bot' ? 'bg-blue-600 text-white rounded-tr-sm' : msg.sender === 'me' ? 'bg-indigo-600 flex-col item-end text-white rounded-tr-sm border border-indigo-400/30' : 'bg-slate-800 text-slate-100 rounded-tl-sm border border-slate-700/50'}`}>
                                            <div className="flex items-center gap-2 mb-2 opacity-50 text-[9px] font-bold uppercase tracking-wider">
                                                {msg.sender === 'bot' ? <Bot className="w-3 h-3" /> : msg.sender === 'me' ? <User className="w-3 h-3 text-indigo-200" /> : <User className="w-3 h-3 text-slate-400" />}
                                                {msg.sender === 'bot' ? 'IA Brain' : msg.sender === 'me' ? 'Human Handoff' : 'Paciente'}
                                            </div>
                                            {msg.message}
                                        </div>
                                    </motion.div>
                                ))}
                                <div ref={messagesEndRef} />
                            </div>

                            <footer className="p-6 bg-[#1e293b] border-t border-slate-800">
                                <form onSubmit={handleSendMessage} className="flex gap-4">
                                    <input
                                        autoFocus
                                        value={draftMessage}
                                        onChange={e => setDraftMessage(e.target.value)}
                                        placeholder="Assuma o controle e responda o lead... (trava a IA)"
                                        className="flex-1 bg-slate-800 border focus:bg-slate-700 border-slate-700 text-slate-200 placeholder:text-slate-500 rounded-xl px-5 py-4 focus:outline-none focus:border-blue-500 transition-colors"
                                    />
                                    <button
                                        type="submit"
                                        disabled={!draftMessage.trim()}
                                        className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold py-4 px-8 rounded-xl flex items-center gap-2 transition-colors disabled:cursor-not-allowed"
                                    >
                                        <Send className="w-4 h-4" /> Enviar
                                    </button>
                                </form>
                            </footer>
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
};

export default ChatMonitor;
