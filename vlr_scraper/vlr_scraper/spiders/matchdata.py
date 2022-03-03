import scrapy

### --- SCRAPER FOR ALL COMPLETED MATCH DATA --- ###


class MatchDataSpider(scrapy.Spider):
    name = "match_data"

    start_urls = [
        "https://www.vlr.gg/42208/guild-esports-vs-oxygen-esports-champions-tour-emea-last-chance-qualifier-lr2"
    ]

    def parse(self, response):
        # extracted from match URL (we will go off of vlr's pk match_#)
        vlr_match_id = int(response.url.split("/")[-2])
        print('Match URL:', response.url.strip())
        print('Match ID:', vlr_match_id)

        disabled_unformatted = response.css(
            'div.vm-stats-gamesnav.noselect div::attr(data-disabled)').getall()
        disabled = []
        for val in disabled_unformatted[1:]:
            disabled.append(int(val))
        print('Disabled Maps (1s):', disabled)

        map_dict_unformatted = response.css(
            'div.vm-stats-gamesnav.noselect div.vm-stats-gamesnav-item.js-map-switch div::text').getall()
        map_dict = []
        disabled_index = 0
        for map in map_dict_unformatted:
            if map.strip() != '':
                if disabled[disabled_index] == 0:
                    map_dict.append(map.strip())
                disabled_index += 1
        print('Map Dict:', map_dict)

        # check if there is valid map data
        bo1 = False
        if not map_dict:
            # single map instance (Bo1)
            if response.css('div.map span::text')[0].get().strip() != '' and response.css('div.map span::text')[0].get().strip() != 'TBD':
                map_dict.append(response.css('div.map span::text')[0].get().strip())
            else:
                map_dict.append('No Map Data')
            bo1 = True
        else:
            map_dict.insert(1, 'All Maps')
        print('Maps:', map_dict)

        i = 1
        map_index = 0
        for tr in response.css('tr')[1:]:
            player_link = tr.css('td.mod-player a::attr(href)').get()
            if player_link is None:
                map_index += 1
                print('\nNext Map')
            else:
                p_url = 'https://www.vlr.gg' + player_link.strip()
                p_id = int(player_link.split('/')[-2])
                p_name = tr.css(
                    'td.mod-player div.text-of::text').get().strip()
                p_team = tr.css('div.ge-text-light::text').get().strip()

                acs = 0 if tr.css('td.mod-stat span.stats-sq::text')[0].get(
                ).strip() == '' else int(tr.css('td.mod-stat span.stats-sq::text')[0].get().strip())

                kills = 0 if tr.css('td.mod-stat.mod-vlr-kills span.stats-sq::text').get(
                ).strip() == '' else int(tr.css('td.mod-stat.mod-vlr-kills span.stats-sq::text').get().strip())

                deaths = 0 if tr.css('td.mod-stat.mod-vlr-deaths span::text')[1].get(
                ).strip() == '' else int(tr.css('td.mod-stat.mod-vlr-deaths span::text')[1].get().strip())

                assists = 0 if tr.css('td.mod-stat.mod-vlr-assists span.stats-sq::text').get(
                ).strip() == '' else int(tr.css('td.mod-stat.mod-vlr-assists span.stats-sq::text').get().strip())

                kd = 0.00 if deaths == 0 else kills / deaths
                kda = 0.00 if deaths == 0 else (kills + assists) / deaths

                diff = 0 if tr.css('td.mod-stat.mod-kd-diff span.stats-sq::text').get(
                ).strip() == '' else int(tr.css('td.mod-stat.mod-kd-diff span.stats-sq::text').get().strip())

                adr = 0 if tr.css('td.mod-stat span.stats-sq.mod-combat::text').get(
                ).strip() == '' else int(tr.css('td.mod-stat span.stats-sq.mod-combat::text').get().strip())

                # data is faulty for older matches, may not use HS%
                hsp = 0 if not tr.css('td.mod-stat span.stats-sq::text')[6].get(
                ).strip() else int(tr.css('td.mod-stat span.stats-sq::text')[6].get().strip('%'))

                fb = 0 if tr.css('td.mod-stat.mod-fb span.stats-sq::text').get(
                ).strip() == '' else int(tr.css('td.mod-stat.mod-fb span.stats-sq::text').get().strip())

                fd = 0 if tr.css('td.mod-stat.mod-fd span.stats-sq::text').get(
                ).strip() == '' else int(tr.css('td.mod-stat.mod-fd span.stats-sq::text').get().strip())

                fb_diff = 0 if tr.css('td.mod-stat.mod-fk-diff span.stats-sq::text').get(
                ).strip() == '' else int(tr.css('td.mod-stat.mod-fk-diff span.stats-sq::text').get().strip())

                print('\nRow', i)
                print('Player ID:', p_id)
                print('Player URL:', p_url)
                print('Name:', p_name)
                print('Team:', p_team)
                map = map_dict[0] if bo1 else map_dict[int(map_index / 2)]
                print('Map:', map)
                print('Match ID:', vlr_match_id)
                print('Stats\n----------')
                print('ACS:', acs)
                print('Kills:', kills)
                print('Deaths:', deaths)
                print('Assists:', assists)
                print('KD:', '{:.2f}'.format(kd))
                print('KDA', '{:.2f}'.format(kda))
                print('+/-:', diff)
                print('ADR:', adr)
                print('HS%:', hsp)
                print('FB:', fb)
                print('FD:', fd)
                print('FB +/-:', fb_diff)
                i += 1
