import scrapy
import re
import os
from scrapy.exporters import CsvItemExporter


URLname = 'loanURLs.csv'
URLdir = os.path.join(os.getcwd(),'../../../loanURLs.csv')

def trim(string):
	try:
		return re.sub('[\s]{2,}','',re.sub('[\t\n]|\s+',' ',string))
	except:
		return ''

def concat(listOfStrings):
	try:
		return trim(' '.join(listOfStrings))
	except:
		return ''

def convertAmount(amountStr):
	if amountStr == '':
		return 0
	else:
		return float(re.sub('[^\d]','',amountStr))

def convertPercentage(percentageStr):
	if percentageStr == 'Funded':
		return 100
	elif percentageStr == 'Expired':
		return 0
	else:
		return float(re.sub('[^\d]','',percentageStr))

class CsvCustomSeperator(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-8'
        kwargs['delimiter'] = '\t'
        super(CsvCustomSeperator, self).__init__(*args, **kwargs)

class loan(scrapy.Item):
    borrowerName = scrapy.Field()
    loanAmount = scrapy.Field()
    percentageFunded = scrapy.Field()
    timeLeft = scrapy.Field()
    amountToGo = scrapy.Field()
    address = scrapy.Field()
    country = scrapy.Field()
    sector = scrapy.Field()
    loanBrief = scrapy.Field()
    noLenders = scrapy.Field()
    loanLength = scrapy.Field()
    repaymentSchedule = scrapy.Field()
    disbursedDate = scrapy.Field()
    fundingModel = scrapy.Field()
    partnerCoverCurLoss = scrapy.Field()
    fieldPartner = scrapy.Field()
    whySpecial = scrapy.Field()
    payInterest = scrapy.Field()
    riskRating = scrapy.Field()
    borrowerStory = scrapy.Field()
    moreAbout = scrapy.Field()
    trustee = scrapy.Field()
    url = scrapy.Field()


class LinksSpider(scrapy.Spider):
    name = 'kivaLoans'
    delimiter = ';'
    allowed_domains = ['kiva.org']
    try:
        with open(URLdir, "rt") as f:
            start_urls = [url.strip()+'?minimal=false' for url in f.readlines()][:20]
    except:
        start_urls = []

    
    print(start_urls[1:3])

    def parse(self, response):
        with open('check2.txt', 'wb') as f:
            f.write(response.body)
        m = loan()
        borrowerName_xpath = '//h1/text()'
        loanAmount_xpath = '//div[@class = "loan-total"]/text()'
        percentageFunded_xpath = '//h2[@class = "green-bolded inline"]/text()'
        timeLeft_xpath = '//div[@class = "days-left-stat "]/text()'
        amountToGo_xpath = '//div[@class = "amount-to-go-stat"]/text()'
        address_xpath = '//div[@class = "country-text columns small-10"]/a/text()'
        country_xpath = '//h2[re:match(text(),".*Country.*")]/text()'
        sector_xpath = '//span[@class = "typeName"]/text()'
        loanBrief_xpath = '//div[@class = "loan-use"]/h2/text()'
        noLenders_xpath = '//a[@class = "lender-count black-underlined"]/text()'
        loanLength_xpath = '//a[text() = "Loan length"]/../following-sibling::div[1]/text()'
        repaymentSchedule_xpath = '//a[text() = "Repayment schedule"]/following-sibling::strong[1]/text()'
        disbursedDate_xpath = '//a[text() = "Disbursed date"]/following-sibling::strong[1]/text()'
        fundingModel_xpath = '//a[text() = "Funding model"]/following-sibling::strong[1]/text()'
        partnerCoverCurLoss_xpath = '//a[text() = "Partner covers currency loss"]/following-sibling::strong[1]/text()'
        fieldPartner_xpath = '//a[text() = "Facilitated by Field Partner"]/following-sibling::strong[1]/text()'
        whySpecial_xpath = '//section[@class = "why-special"]/div[2]/div/text()'
        payInterest_xpath = '//a[text() = "Is borrower paying interest"]/following-sibling::strong[1]/text()'
        riskRating1_xpath = '//div[@id = "field-partner-risk-rating"]/strong/svg[@class = "icon icon-star"]'
        riskRating2_xpath = '//div[@id = "field-partner-risk-rating"]/strong/svg[@class = "icon icon-half-star"]'
        borrowerStory_xpath = '//section[@class = "loan-description"]//text()'
        moreAbout_xpath = '//div[@id = "ac-more-loan-info-body"]//text()'
        trustee_xpath = '//h2[re:match(text(),".*Trustee.*")]/text()'

        m['url'] = response.request.url
        m['borrowerName'] = response.xpath(borrowerName_xpath).get()
        m['loanAmount']  = convertAmount(trim(response.xpath(loanAmount_xpath).get()).replace('Total loan: ',''))
        m['percentageFunded'] = convertPercentage(trim(response.xpath(percentageFunded_xpath).get()))
        m['timeLeft'] = trim(response.xpath(timeLeft_xpath).get())
        m['amountToGo'] = convertAmount(trim(response.xpath(amountToGo_xpath).get()).replace(' to go',''))
        m['address'] = trim(response.xpath(address_xpath).get())
        m['country'] = trim(response.xpath(country_xpath).get()).replace('Country: ','')
        m['sector'] = trim(response.xpath(sector_xpath).get())
        m['loanBrief'] = trim(response.xpath(loanBrief_xpath).get())
        m['noLenders'] = convertAmount(trim(response.xpath(noLenders_xpath).get()))
        m['loanLength'] = trim(response.xpath(loanLength_xpath).get())
        m['repaymentSchedule'] = trim(response.xpath(repaymentSchedule_xpath).get())
        m['disbursedDate'] = trim(response.xpath(disbursedDate_xpath).get())
        m['fundingModel'] = trim(response.xpath(fundingModel_xpath).get())
        m['partnerCoverCurLoss'] = trim(response.xpath(partnerCoverCurLoss_xpath).get())
        m['fieldPartner'] = trim(response.xpath(fieldPartner_xpath).get())
        m['whySpecial'] = trim(response.xpath(whySpecial_xpath).get())
        m['payInterest'] = trim(response.xpath(payInterest_xpath).get())
        m['borrowerStory'] = concat(response.xpath(borrowerStory_xpath).getall())
        m['moreAbout'] = concat(response.xpath(moreAbout_xpath).getall())
        m['trustee'] = trim(response.xpath(trustee_xpath).get())
        m['riskRating'] = len(response.xpath(riskRating1_xpath).getall())/2 + len(response.xpath(riskRating2_xpath).getall())/4
        
        yield m

