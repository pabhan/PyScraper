import HTMLParser
import urllib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

struct_list = []
content_list = []
href = []
to_ignore = ["div","img","li","meta","ul","tr","td","style","script","stile","link","th","span"]
blacklist = dict(zip(to_ignore,range(1,len(to_ignore))))

#IO utilities
def getHTMLFromUrl(url):
	return urllib.urlopen(url).read()
def exportTextToFile(text,file):
	open(file,"a").write(text)

#Parsing utilities
def parseUrl(url):
	text = getHTMLFromUrl(url)
	aParser = parser(url)
	aParser.feed(text)
	return {"struct_list":struct_list, "content_list":content_list, "links":href}

def elaborateRef(obj,ref):
	ref_tokens = ref.split("/")
	l = len(ref_tokens)
	if ref_tokens[0] == "http:" or ref_tokens[0] == "https:":
		return ref
	url_tokens = obj.originalUrl.split("/")
	i = 0
	ref_sp = ref_tokens[i]
	while not ref_sp:
		i+=1
		if i<l:
			ref_sp = ref_tokens[i]
		else:
			return ""
	new_url = []
	if ref_sp[0] == "#":
		new_url = url_tokens
		new_url[-1]+=ref_sp
		new_url.extend(ref_tokens[i+1:])
	else:
		flag = 0
		for token in url_tokens:
			if token == ref_sp:
				new_url.extend(ref_tokens[i+1:])
				flag = 1
				break
			else:
				new_url.append(token)			
		if flag == 0:
			new_url.extend(ref_tokens[i:])
	return "/".join(new_url)

#fine tuning parameters
def getBlacklist():
	return blacklist

def addToBlacklist(tag):
	blacklist.append(tag)
	
def removeFromBlackList(tag):
	blacklist.pop(tag)


	
#main interface implementation
class parser(HTMLParser.HTMLParser):
	
	def __init__(self,url):
		self.convert_charrefs= True
		self.reset()
		self.originalUrl = url

	def handle_starttag(self,tag, attrs):
		struct_list.append(tag)
		for attr in attrs:
			if attr[0]=="href":
				href.append(elaborateRef(self,attr[1]))

#	def handle_endtag(tag)
#	#This method is called to handle the end tag of an element (e.g. </div>).
#	#The tag argument is the name of the tag converted to lower case.
		
#	def handle_startendtag(tag, attrs)
#	#Similar to handle_starttag(), but called when the parser encounters an XHTML-style empty tag (<img ... />). 
#	#This method may be overridden by subclasses which require this particular lexical information; the default implementation simply calls handle_starttag() and handle_endtag().

	def handle_data(self,data):
	#This method is called to process arbitrary data (e.g. text nodes and the content of <script>...</script> and <style>...</style>).
		content_list.append(data)
#	def handle_entityref(name)
#	#This method is called to process a named character reference of the form &name; (e.g. &gt;), where name is a general entity reference (e.g. 'gt').
		
#	def handle_charref(self,name):
#	#This method is called to process decimal and hexadecimal numeric character references of the form &#NNN; and &#xNNN;. 
#	#For example, the decimal equivalent for &gt; is &#62;, whereas the hexadecimal is &#x3E;; in this case the method will receive '62' or 'x3E'.
	
#	def handle_comment(data)
	#This method is called when a comment is encountered (e.g. <!--comment-->).
	#For example, the comment <!-- comment --> will cause this method to be called with the argument ' comment '.
	#The content of Internet Explorer conditional comments (condcoms) will also be sent to this method, so, for <!--[if IE 9]>IE9-specific content<![endif]-->, 
	#this method will receive '[if IE 9]>IE-specific content<![endif]'.

#	def handle_decl(decl)
	#This method is called to handle an HTML doctype declaration (e.g. <!DOCTYPE html>).
	#The decl parameter will be the entire contents of the declaration inside the <!...> markup (e.g. 'DOCTYPE html').

#	def handle_pi(data)#This method is called when a processing instruction is encountered. The data parameter will contain the entire processing instruction. For example, for the processing instruction <?proc color='red'>, this method would be called as handle_pi("proc color='red'").#Note#The HTMLParser class uses the SGML syntactic rules for processing instructions. An XHTML processing instruction using the trailing '?' will cause the '?' to be included in data.

#	def unknown_decl(data)#This method is called when an unrecognized declaration is read by the parser.




if __name__ == "__main__":
	f = parser("http://en.wikipedia.org/wiki/Main")

	# urltext = urllib.urlopen("https://www.ilsole24ore.it").read()
	# aParser = parser()
	# aParser.feed(urltext)
	# s = ""
	# for it in range(0,len(struct_list)-1):
		# if struct_list[it] == "a":
			# s+= content_list[it]
	# for l in href:
		# if l[:6] == "/watch":
			# s+=l+"\n"
	# open("maradona.txt","w").write(s)