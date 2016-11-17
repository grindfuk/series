# run this file to obtain test stats + a score for a specific repo

import unittest
#from all_tests import *
import all_tests

if __name__ == '__main__':
    #unittest.main(module=all_tests, exit=False)
	suite = unittest.TestLoader().loadTestsFromModule(all_tests)
	tr = unittest.TextTestRunner(verbosity=0, descriptions=False,buffer=True).run(suite)


	# compute for each category the score
	arithmetic_score = 0
	accessor_score = 0
	lazy_score = 0
	doc_score = 0

	for score in all_tests.scores:
		if '#ac' in score[0]:
			accessor_score += score[2]
		if '#ar' in score[0]:
			arithmetic_score += score[2]
		if '#lz' in score[0]:
			lazy_score += score[2]
		if '#dc' in score[0]:
			doc_score += score[2]

	# print results
	print('-----------------------------------')
	print('ac score: {}P'.format(accessor_score))
	print('ar score: {}P'.format(arithmetic_score))
	print('lz score: {}P'.format(lazy_score))
	print('dc score: {}P'.format(doc_score))
	print('-----------------------------------')
	print('stats:')
	print('-----------------------------------')
	print('errors: \t{}'.format(len(tr.errors)))
	print('failures: \t{}'.format(len(tr.failures)))
	print('score stats:')

	total_score = 0
	for score in all_tests.scores:
		print('{}: {} \t {} P'.format(score[0], score[1], score[2]))
		total_score += score[2]

	print('-----------------------------------')
	print('total score: {}P'.format(total_score))

