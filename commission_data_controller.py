import datetime
import discord


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
    
    def commission_list_embed_creator(self, interaction, pais):
        country_name, embed_color = self.country_id_handler(pais)

        embed = discord.Embed(title=f"**Lista de Ciclo de {country_name}**", description=f"Confira sua lista de comissões no ciclo atual de {country_name}", color=embed_color)

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)

        embed.add_field(name="#1\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#2\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#3\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#4\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#5\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#1\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#2\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#3\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#4\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#5\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#1\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#2\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#3\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#4\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#5\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#1\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#2\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#3\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#4\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#5\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#1\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#2\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#3\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#4\tComunicação via Poemas", value="Feito: 4/4", inline=False)
        embed.add_field(name="#5\tComunicação via Poemas", value="Feito: 4/4", inline=False)

        embed.set_footer(text=f"Informação requisitada por: {interaction.user.display_name}")
        embed.timestamp = datetime.datetime.now()

        return embed
    
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