import datetime
import discord
from discord import ButtonStyle
from discord.ui import Button, View
import class_extensions as ce


class commission_data_controller():
    def __init__(self):
        pass
    
    def commission_list_handler(self, list):
        # Dividindo a string em linhas
        linhas = list.strip().split('\n')

        # Inicializando a lista indexada
        lista_indexada = []

        # Processando as linhas
        for linha in linhas:
            # Dividindo cada linha em partes usando a vírgula
            item = linha.strip().split('\t')
            
            id = int(item[0])
            nome = item[1].encode('utf-8').decode('utf-8')
            descricao = item[2]
            frequencia = int(item[3])
            ocorrencias = int(item[4])
            bloqueada = item[5].lower() == 'true'

            # Adicionando à lista indexada
            lista_indexada.append([id, nome, descricao, frequencia, ocorrencias, bloqueada])
        
        return lista_indexada
    
    def short_commission_list_handler(self, list):
        # Dividindo cada linha em partes usando a vírgula
        item = list.strip().split('\t')
        
        bloqueadas = int(item[2])
        frequencia = int(item[0]) - bloqueadas
        ocorrencias = int(item[1])

        # Adicionando à lista indexada
        lista_indexada = [frequencia, ocorrencias, bloqueadas]
        
        return lista_indexada
    
    def commission_list_embed_creator(self, interaction, pais, data: list, current_page: int = 1, commissions_per_page: int = 10, short: bool = False):
        country_name, embed_color = self.country_id_handler(pais)

        embed = discord.Embed(title=f"**Lista de Ciclo de {country_name}**", description=f"Confira sua lista de comissões no ciclo atual de {country_name}", color=embed_color)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)

        start_index = (current_page - 1) * commissions_per_page
        end_index = (current_page * commissions_per_page) - 1

        if(short):
            embed.add_field(name=f"Progresso no Ciclo Atual: {data[1]} / {data[0]}", value = f"Comissões Bloqueadas: {data[2]}", inline=False)
        else:
            for commission in data[start_index : end_index]:
                embed.add_field(name=f"#{commission[0]}\t{commission[1]}", value=f"Feito: {commission[4]}/{commission[3]}", inline=False)

        embed.set_footer(text=f"Informação requisitada por: {interaction.user.display_name}")
        embed.timestamp = datetime.datetime.now()
        

        return embed
    
    def commission_list_view_creator(self, current_page: int = 1, number_of_pages: int = 1):
        if(number_of_pages == 1): return View()

        view = ce.View()
        
        button_back = Button(label="Página Anterior", style=ButtonStyle.primary, disabled=(True if current_page == 1 else False))
        button_page = Button(label=f"{current_page}/{number_of_pages}", disabled=True, style=ButtonStyle.gray)
        button_frwd = Button(label="Próxima Página", style=ButtonStyle.primary, disabled=(True if current_page == number_of_pages else False))
        
        view.add_items(button_back, button_page, button_frwd)
        # view.add_item(button_back)
        # view.add_item(button_page)
        # view.add_item(button_frwd)

        return view
    
    def country_id_handler(self, id):
        match id:
            case 1:
                country_name = "Mondstadt"
                embed_color = 0x00ffff
            case 2:
                country_name = "Liyue"
                embed_color = 0xffff00
            case 3:
                country_name = "Inazuma"
                embed_color = 0x9510e6
            case 4:
                country_name = "Sumeru"
                embed_color = 0x10ee22
            case 5:
                country_name = "Fontaine"
                embed_color = 0x1022ee
        
        return country_name, embed_color