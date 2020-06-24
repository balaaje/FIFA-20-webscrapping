# -*- coding: utf-8 -*-
import scrapy


class SofifaSpider(scrapy.Spider):
    name = 'sofifa'
    allowed_domains = ['sofifa.com']
    start_urls = ['https://sofifa.com/players?col=oa&sort=desc&showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gk&showCol%5B54%5D=gp&showCol%5B55%5D=gr&showCol%5B56%5D=tt&showCol%5B57%5D=bs&showCol%5B58%5D=wk&showCol%5B59%5D=sk&showCol%5B60%5D=aw&showCol%5B61%5D=dw&showCol%5B62%5D=ir&showCol%5B63%5D=pac&showCol%5B64%5D=sho&showCol%5B65%5D=pas&showCol%5B66%5D=dri&showCol%5B67%5D=def&showCol%5B68%5D=phy&offset=0']

    def parse(self, response):
        headers = response.css('table.table>thead>tr>th ::text').extract()[7:]

        for player in response.css('table.table>tbody>tr'):
            item = {}
            item['Name'] = player.css("td.col-name a::attr(data-tooltip)").extract()
            item['Image'] = player.css('figure.avatar>img::attr(data-src)').get()
            item['Country'] = player.css('td.col-name>a>div>img').xpath('@title').extract()
            item['Position'] = ','.join(player.css('td.col-name span.pos ::text').extract())
            item['Age'] = player.css('td.col-ae ::text').get()
            item['Overall'] = player.css('td.col-oa ::text').get()
            item['Potential'] = player.css('td.col-oa ::text').get()
            item['Club'] = player.css('td.col-name')[1].css('a ::text').get()
            item['Contract']=player.css("td>div>div ::text").extract()

            value = list(map(str.strip, [p.css(' ::text').get() for p in player.css('td')[7:]]))
            item.update(dict(zip(headers, value)))
            yield item
        next_page = response.xpath('//span[@class="bp3-button-text" and text()="Next"]/parent::a/@href').get()
        if next_page is not None:
            #next_page=response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)