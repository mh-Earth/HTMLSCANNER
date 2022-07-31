from fake_http_header import FakeHttpHeader
import sys
import requests
from bs4 import BeautifulSoup,Comment
import time 
import argparse
from argparse import RawTextHelpFormatter
from colorama import init, Fore
import ast
init(convert=True)

# COLORS
W = Fore.RESET
R = Fore.RED
RL = Fore.LIGHTRED_EX
G = Fore.GREEN
GL = Fore.LIGHTGREEN_EX
C = Fore.CYAN
CL = Fore.LIGHTCYAN_EX
Y = Fore.YELLOW
YL = Fore.LIGHTYELLOW_EX
BL = Fore.LIGHTBLUE_EX

import requests


class WebRequest():
    def __init__(self,url,httpHeader=None,params=None) -> None:
        self.url = url
        self.httpHeader = httpHeader
        self.params = params
        self.fake_header = FakeHttpHeader()
        self.fake_header_dict = self.fake_header.as_header_dict()
    def webResponse(self):
        try:
            res = requests.get(self.url,headers=self.fake_header_dict,params=self.params)
        except Exception as e:
            print(RL + "Failed to establish a new connection" +"\n"+str(e) + W)
            
            sys.exit()
        
        if res.status_code == 200:
            return res
        else:
            raise ConnectionError(res.status_code)


class HtmlEdit():
    def __init__(self,response) -> None:
        self.Response = response
        self.htmlContent = self.Response.text
        self.htmlHeaders = self.Response.headers
        self.soup = BeautifulSoup(self.htmlContent,"html.parser")

    def header(self):
        print(f'{GL}[+]{self.htmlHeaders} {W}')
    
    def htmlView(self,prettify=False):
        if prettify:
            print(BeautifulSoup(self.htmlContent,"html.parser").prettify())
        
        else:
            print(self.htmlContent)

    # Extract all href links
    def extractLink(self,mood=int) -> None:
        self.total_links = 0
        # 0 show all links 
        if mood == 0:
            for links in self.soup.find_all('a', href=True):
                if links != None:
                    print( GL + '[+]'  + GL + " " + links.get("href") + " | "  + CL + "InnerHtml=" + GL + links.text.replace("\n","").replace(" ","") + W)
                time.sleep(.1)
                self.total_links += 1
            self.otherLinks()
        
        elif mood == 4:
            self.otherLinks()

        elif mood != 0:
            print(f"{YL}[++] HREF LINKS {W}")
            for links in self.soup.find_all('a', href=True):

                if mood == 1:
                    if links != None and links.get("href"):
                        print( GL + '[+]'  + GL + " " + links.get("href") + " | "  + CL + "InnerHtml=" + GL + links.text.replace("\n","").replace(" ","") + W)
                        self.total_links += 1

                elif mood == 2:
                    if links != None and links.get("href").startswith('http'):
                        print( GL + '[+]'  + GL + " " + links.get("href") + " | "  + CL + "InnerHtml=" + GL + links.text.replace("\n","").replace(" ","") + W)
                        self.total_links += 1

                elif mood == 3:
                    if links != None and not links.get("href").startswith('http'):
                        print( GL + '[+]'  + GL + " " + links.get("href") + " | "  + CL + "InnerHtml=" + GL + links.text.replace("\n","").replace(" ","") + W)
                        self.total_links += 1
                else:
                    print(f'{RL}[-] --l Mood {mood} not found {W}')
                    return
                
                time.sleep(.05)

        print(f'{RL}[++]{GL} Total link found {self.total_links} {W}')
            

    # Extract img.scr,actions links
    def otherLinks(self):
        print(YL + "[++]" + " IMAGE LINKS" + W)
        for links in self.soup.find_all("img"):
            print(f'{GL} {links.get("src")} | {CL} {links.get("alt")} {W}' )
            self.total_links += 1
            time.sleep(.1)
            
        print(f'{YL}[++] Form links{W}')
        for i in self.soup.find_all("form"):
            print(f'{GL}[+] {i.get("action")}{W}')
            self.total_links += 1
            time.sleep(.1)

        print(f'{YL}[++] Link Tags{W}')
        for i in self.soup.find_all("link"):
            print(f'{GL}[+] {i.get("href")}{W}')
            self.total_links += 1
            time.sleep(.1)


    def getForm(self):
        print(f'{YL}[++] Total form found {len(self.soup.find_all("form"))}')
        if len(self.soup.find_all("form")) > 0:
            print(f'{YL}[++] Showing Form details\n')
            for index,forms in enumerate(self.soup.find_all("form")):
                print(f'{CL}[++] Form {index+1}:{W}')
                print(f'    {GL}Action={forms.get("action")}')
                for index,inputs in enumerate(forms.find_all("input")):
                    print(f'    {YL}[{index+1}] {GL} {str(inputs).replace(" ","|")}')
                    time.sleep(.05)

                for index,inputs in enumerate(forms.find_all("button")):
                    print(f'    {YL}[{index+1}] {GL} {str(inputs).replace(" ","|")}')
                    time.sleep(.05)
                print('----------------------------------------------------------------------------------------------------------')
                time.sleep(.1)

    def getInputsArea(self):
        print(f'{YL}[++] Total input area found {len(self.soup.find_all("input"))}')
        if len(self.soup.find_all("input")) > 0:
            for inputTag in self.soup.find_all("input"):
                print( GL + str(inputTag).replace(" "," | ") + W)
                time.sleep(.1)

    def tagCounter(self,showDetails=False):
        tag_list = []
        # gathering all used tag in the page
        for tag in self.soup.findAll(True):
            tag_list.append(tag.name)
        print(f"{GL}[+] TAGS FOUND {RL}{len(tag_list)}")

        if showDetails:
            # removing duplicate item
            tag_list = list(sorted(set(tag_list)))
            # Showing tag list
            print(GL + "[+]",end=" ")
            for tag in tag_list:
                print(f"{GL}{tag.capitalize()}={len(self.soup.find_all(tag))} {RL}|{W} ",end='')
                time.sleep(.03)


    def name_tagCounter(self,tag_name,showDetails=False):
        print(f'{YL}[+] Total "{tag_name}" tag found {len(self.soup.find_all(tag_name))}{W}')
        if showDetails:
            for i in self.soup.find_all(tag_name):
                print(f"{GL}{i}{W}")
                time.sleep(.1)


    def getTitle(self):
        title = self.soup.find('title').text
        print(YL + "Title::" +title + W)
        # return title
        
    
    def findComments(self):
        comments = self.soup.findAll(text = lambda text: isinstance(text, Comment))
        
        if len(comments) <= 0:
            print(f'{RL}[+] NO COMMENTS FOUND...')
            return

        for i in comments:
            print(f"{YL}[+] {GL}{i.strip()}{W}")

    def scanComments(self):
        comments = self.soup.findAll(text = lambda text: isinstance(text, Comment))
        if len(comments) <= 0:
            print(f'{RL}[+] NO COMMENTS FOUND...')
            return

        commentSoup = BeautifulSoup(str(comments),"html.parser")
    

        print(f'{YL}[++] URL PATHS FOUND IN COMMENTS')
        for i in commentSoup.find_all("a",href=True):
            print(f'{GL}-- {i.get("href")} | {i.text}{W}')
            time.sleep(.1)

        print(f'{YL}[++] SCRIPT TAG FOUND IN COMMENT')
        for i in commentSoup.find_all("script"):
            print(f"{GL}-{i}{W}")
            time.sleep(.1)

        print(f'{YL}[++] STYLE TAG FOUND IN COMMENT')
        for i in commentSoup.find_all("style"):
            print(f"{GL}-{i}{W}")
            time.sleep(.1)

        print(f'{YL}[++] SCRIPT TAG FOUND IN COMMENT')
        for i in commentSoup.find_all("link"):
            print(f"{GL}-{i}{W}")
            time.sleep(.1)

    def smartScan(self,showDetails,linkMood):
        self.getTitle()
        print("\n")
        self.tagCounter(showDetails=showDetails)
        print("\n")
        self.extractLink(mood=linkMood)
        print("\n")
        self.getForm()
    
    def fullScan(self,linkMood,showDetails):
        self.header()
        self.getTitle()
        self.tagCounter(showDetails=showDetails)
        print("\n")
        self.extractLink(mood=linkMood)
        print("\n")
        self.getForm()
        print("\n")
        self.getInputsArea()
        print("\n")
        self.findComments()




def main(args):
    print(args)
    # print(type(args.header))
    if args.header != False or args.params != False:
        header = ast.literal_eval(args.header)
        responsesClass = WebRequest(args.u,httpHeader=header,params=args.params).webResponse()
    else:
        responsesClass = WebRequest(args.u).webResponse()

    main = HtmlEdit(responsesClass)
    # return
    if args.F:
        main.fullScan(linkMood=0 if args.l=="" else int(args.l),showDetails=True if args.all else False)
        return
    
    if args.s:
        main.smartScan(linkMood=2 if args.l=="" else int(args.l),showDetails=True if args.all else False)
        return

    if args.p:
        if args.pP == False:
            main.htmlView(prettify=False)

    if args.pP == "":
        if args.p == False:
            main.htmlView(prettify=True)

    if args.h:
        main.header()

    if args.c:
        main.findComments()

    if args.cS:
        main.scanComments()

    if args.t:
        main.getTitle()
        
    if args.cT:
        main.tagCounter(showDetails=True if args.all == "" else False)
        
    if args.fT:
        main.name_tagCounter(args.fT.lower(),showDetails=True if args.all == "" else False)
    
    if args.l:
        if args.l == "":
            args.l = "2"
        # print("something")
        args.l = int(args.l)
        if args.l == 0:
            main.extractLink(mood=args.l)
        elif args.l == 1:
            main.extractLink(mood=args.l)
        elif args.l == 2:
            main.extractLink(mood=args.l)
        elif args.l == 3:
            main.extractLink(mood=args.l)
        elif args.l == 4:
            print("This is a mood 4")
            main.extractLink(mood=args.l)

    return "Exit..."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='test', formatter_class=RawTextHelpFormatter)

    parser.add_argument('--u',type=str,required=True,help="Website url")
    parser.add_argument('--s',type=str,help="Smart Scan" ,default=False ,nargs='?', const=True)
    parser.add_argument('--h',type=str,help="View Headers" ,default=False ,nargs='?', const=True)
    parser.add_argument('--p',type=str,help="View html content" ,default=False ,nargs='?', const=True)
    parser.add_argument('--pP',type=str,help="View html content (Formatted)" ,default=False ,nargs='?', const=True)
    parser.add_argument('--F',type=str,help="Full Scan" ,default=False ,nargs='?', const=True)
    parser.add_argument('--all',type=str,help="Show details" ,default=False,nargs='?', const=True)
    parser.add_argument('--c',type=str,help="Search for comments" ,default=False ,nargs='?', const=True)
    parser.add_argument('--cS',type=str,help="Smart search for comments" ,default=False,nargs='?', const=True)
    parser.add_argument('--t',type=str,help="Get title" ,default=False ,nargs='?', const=True)
    parser.add_argument('--cT',type=str,help="Tag count" ,default=False ,nargs='?', const=True)
    parser.add_argument('--fT',type=str,help="Get Tag details" ,default=False ,nargs='?', const=True)
    parser.add_argument('--l',type=str,help="Extract links\nMood:\n1=All href links \n2= Https/Http links \n3= Internal server links \n4= Other links \n0=Everything" ,default=False ,nargs='?', const='')
    parser.add_argument('--header',type=str,help="Add Headers" ,default=False)
    parser.add_argument('--params',type=str,help="Add Parameters" ,default=False)

    args = parser.parse_args()
    sys.stdout.write(str(main(args)))




