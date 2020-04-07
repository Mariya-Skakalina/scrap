import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        self.page = 0
        url = 'ссылка'
        yield scrapy.Request(url, self.parse)

    def parse_company(self,response):
        res = {}
        for quote in response.css('div.col-md'):
            name_company = quote.css('h1::text').get()
            if name_company is not None:
                res['name'] = name_company
                break
        contacts = []
        for quote in response.css('div.company-info-details div'):
            contact = quote.css('span a::text').get()
            if contact is not None:
                contacts.append(contact)

        ids = 0
        if len(contacts) > 0:
            for i in contacts:
                res[f'contact_{ids}'] = i
                ids += 1
        yield res

    def parse(self, response):
        res = []
        for quote in response.css('div.result-content'):
            url = quote.css('h3 a::attr(href)').get()
            if url is not None:
                yield response.follow(url, self.parse_company)
        # 12 страниц по 20 элементов, пагинация происходить путем передачи параметра 
        # limitstart(что говорит о том с какого элемента выводит результат, 1 страница это от 1 до 20, 2 страница от 20 до 40 и т.д.) в форме
        if self.page <= 240:
            self.page += 20
            yield scrapy.FormRequest(
                url='ссылка',
                method='GET',
                formdata={'limit': '20', 
                    'limitstart': str(self.page), 
                    'task': 'searchCompaniesByName', 
                    'option': 'com_jbusinessdirectory', 
                    'controller': 'search', 
                    'categories': '',
                    'view': 'search', 
                    'categoryId':'216',
                    'searchkeyword': '',
                    'letter': '',
                    'categorySearch': '',
                    'citySearch': '',
                    'regionSearch': '',
                    'areaSearch': '',
                    'provinceSearch':'' ,
                    'countrySearch': '',
                    'typeSearch': '',
                    'zipcode': '',
                    'geo-latitude': '',
                    'geo-longitude': '',
                    'radius': '',
                    'featured': '',
                    'filter-by-fav': '',
                    'filter_active': '',
                    'selectedParams': '',
                    'form_submited': '1',
                    'moreParams': '',
                    'preserve': '',
                    'orderBy': 'id desc'},
                callback=self.parse
            )
                