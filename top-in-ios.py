import sys, getopt, re
import codecs
import json
import cgi
import pprint

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def usage():
	print '%s -i INPUT -o OUTPUT -f FILTER' % (sys.argv[0])

def is_ios(repo):
	sys.stderr.write("%s\n"%(repo['name']))
	for x in ['ios', 'ipad', 'iphone']:
		for y in ['name', 'description']:
			if repo['name'] == 'RecordMyScreen':
				sys.stderr.write("%s,%s\n" % (x, y))
			if re.search(x, repo[y], re.I) != None:
				return True

	return False

def is_android(repo):
	return re.search('android', repo['name'], re.I) != None or re.search('android', repo['description'], re.I) != None
	
def main(argv):
        try:
                opts, args = getopt.getopt(argv[1:], 'i:o:f:', ['input=','output=','filter='])
        except getopt.GetoptError:
                usage()
                sys.exit(2)

	infile = None
	outfile = None
	filt = None
	
        for o, a in opts:
                if o == '-i':
			infile = a
		elif o == '-o':
			outfile = a
		elif o == '-f':
			filt = a

	if not infile:
		sys.exti(2)

	content = open(infile, 'rt').read()
	repos = json.loads(content)
	filter_func = {'ios':is_ios, 'android':is_android}[filt]
	repos = sorted(repos, key=lambda x: int(x['forks'].replace(',','')), reverse=True)
	for repo in repos:
		if filter_func(repo):
                        print '* [%s](%s)' % (cgi.escape(repo['name']), repo['html_url'])
                        print
                        #print '    license:`%s`' % (repo['license'])
                        #print
                        print '    stared:`%s`, forks:`%s`, issues:`%s`, pushed:`%s`' % (repo['watchers_count'], repo['forks'], repo['open_issues_count'], repo['pushed_at'])
                        print
                        print '    %s' % (cgi.escape(repo['description']))
                        print


if __name__ == '__main__':
	main(sys.argv)
