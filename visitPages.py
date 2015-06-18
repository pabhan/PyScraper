from parsing import * 
import sys,math,random


if __name__=="__main__":
	logFile = "explored.dat"
	try:
		N = int(sys.argv[2])
	except:
		N = 50
	
	i = 0
#	parsed_items = parseUrl(sys.argv[1])
	if sys.argv[1] == "":
		origin = "http://en.wikipedia.org/wiki/Blackjack"
	else:
		origin = sys.argv[1]
	
	past = origin
	parsed_items = parseUrl(past)["links"]
	current = parsed_items[int(math.floor(random.random()*len(parsed_items)))]

	while i<N:
		max = len(parsed_items)
		it = 1
		while it<max:
			try:
				con = urllib.urlopen(current)
				exportTextToFile("OK\t "+current+"\n",logFile)
				if past == current:
					parsed_items = parseUrl(origin)["links"]
					current = parsed_items[int(math.floor(random.random()*len(parsed_items)))]				
				else:
					parsed_items = parseUrl(current)["links"]
					current = parsed_items[int(math.floor(random.random()*len(parsed_items)))]
				it = max
			except:
				exportTextToFile("KO\t "+current+"\n",logFile)
				current = parsed_items[it]
				it +=1
		i+=1
