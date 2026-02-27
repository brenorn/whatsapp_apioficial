from PIL import Image


class ImageWithBorder:
    @staticmethod
    def create_bordered_image(image_path, border_path, output_path, target_size=(1080, 1080)):
        """
        Cria a imagem com a borda e salva no caminho especificado.

        Args:
            image_path (str): Caminho da imagem base.
            border_path (str): Caminho da borda.
            output_path (str): Caminho para salvar a imagem resultante.
            target_size (tuple): Dimensão alvo para o corte central (largura, altura).
        Returns:
            str: Caminho da imagem resultante.
        """
        center_size = (843, 843)
        offset_x = 117
        offset_y = 69
        image = Image.open(image_path)
        border = Image.open(border_path)

        # Redimensionar proporcionalmente para cobrir o centro (843x843)
        img_ratio = image.width / image.height
        target_ratio = center_size[0] / center_size[1]

        if img_ratio > target_ratio:
            # Foto mais larga: ajusta altura, corta laterais
            new_height = center_size[1]
            new_width = int(new_height * img_ratio)
        else:
            # Foto mais alta: ajusta largura, corta topo/baixo
            new_width = center_size[0]
            new_height = int(new_width / img_ratio)

        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Crop central da foto para 843x843
        left = (new_width - center_size[0]) // 2
        top = (new_height - center_size[1]) // 2
        right = left + center_size[0]
        bottom = top + center_size[1]
        cropped_image = image.crop((left, top, right, bottom))

        # Garantir RGBA
        if cropped_image.mode != 'RGBA':
            cropped_image = cropped_image.convert('RGBA')
        if border.mode != 'RGBA':
            border = border.convert('RGBA')

        result = border.copy()
        result.paste(cropped_image, (offset_x, offset_y))
        result.paste(border, (0, 0), mask=border.split()[3] if border.mode == 'RGBA' else None)
        result.save(output_path)
        return output_path
