import multiprocessing as mp
import re
import requests

max_requests = 20
src_file = "urls.txt"
results = []
search_term = "news"
dest_file = "results_" + search_term + ".txt"

def website_searcher( url ):
	try:
		resp = requests.get( url[1], timeout=5 )
	except Exception as e:
		return (url[0], url[1], False)

	# only if page was succesfully fetched
	if resp.status_code == 200:
		num_occ = len(re.findall(search_term.lower(), resp.text.lower()))
		return (url[0], url[1], True if num_occ else False)
	else:
		return (url[0], url[1], False)

def main():
	urls = []

	# reading src_file
	with open( src_file, 'r' ) as fp:
		_ = fp.readline()
		for line in fp:
			tokens = line.split(",")
			urls.append( [tokens[0], "http://www.{}".format(tokens[1].strip('"'))] )

	r = []
	with mp.Pool(max_requests) as p:
		r = p.map(website_searcher, urls )

	# writing results to dest_file
	with open(dest_file, 'w') as fp:
		for i in r:
			fp.write( str(",".join(str(ix) for ix in i))+"\n" )


if __name__ == '__main__':
	main()
