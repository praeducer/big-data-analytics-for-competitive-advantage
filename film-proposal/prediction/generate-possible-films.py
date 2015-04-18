# description: generate all possible combinations of films given predictive features
# author: Paul Prae

# TODO: What did I use?
import os
import sys
import csv
import ntpath


if __name__=="__main__":

	outputFile = './data/possible_films.csv'
	filmWriter = csv.writer(open(outputFile, 'w', newline=''))


	# TODO: make sure the order of the for loops are the same as the order of the headers
	rowHeaders = ['Budget']
	actors = ['Actor_Morgan_Freeman','Actor_Dennis_Hopper','Actor_Henry_Fonda','Actor_Bruce_Willis','Actor_Samuel_L__Jackson','Actor_Robert_De_Niro','Actor_Burt_Lancaster','Actor_Donald_Sutherland','Actor_Christopher_Lee','Actor_John_Wayne','Actor_Keanu_Reeves','Actor_Nick_Nolte','Actor_Nicolas_Cage','Actor_Gene_Hackman','Actor_Michael_Caine','Actor_Sean_Connery','Actor_Oliver_Hardy','Actor_Stan_Laurel','Actor_Robert_Duvall','Actor_Susan_Sarandon','Actor_Jack_Nicholson','Actor_Robert_Downey_Jr_','Actor_Christopher_Walken','Actor_Willem_Dafoe','Actor_James_Stewart','Actor_Dustin_Hoffman','Actor_Robin_Williams','Actor_John_Goodman','Actor_Dennis_Quaid','Actor_Harvey_Keitel']
	rowHeaders.extend(actors)
	filmWriter.writerow(rowHeaders)

	budgetValues = [100000000,200000000]
	actorValues = {
		'Actor_Morgan_Freeman':		[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Dennis_Hopper':		[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Henry_Fonda':		[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Bruce_Willis':		[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Samuel_L__Jackson': 	[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Robert_De_Niro': 	[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Burt_Lancaster': 	[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Donald_Sutherland': 	[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Christopher_Lee': 	[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_John_Wayne': 		[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Keanu_Reeves': 		[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Nick_Nolte': 		[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Nicolas_Cage': 		[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Gene_Hackman': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Michael_Caine': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Sean_Connery': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Oliver_Hardy': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Stan_Laurel': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Robert_Duvall': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
		'Actor_Susan_Sarandon': 	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
		'Actor_Jack_Nicholson': 	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
		'Actor_Robert_Downey_Jr_': 	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
		'Actor_Christopher_Walken': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
		'Actor_Willem_Dafoe': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
		'Actor_James_Stewart': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
		'Actor_Dustin_Hoffman': 	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
		'Actor_Robin_Williams': 	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		'Actor_John_Goodman': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
		'Actor_Dennis_Quaid': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
		'Actor_Harvey_Keitel': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
	}

	count = 0
	# TODO: make sure the order of the for loops are the same as the order of the headers
	for budget in budgetValues:

		for actor in actors:

			# this all should only be on the inner most loop
			count += 1
			print(count)

			currentRow = []
			currentRow.append(budget)
			currentRow.extend(actorValues[actor])
			
			filmWriter.writerow(currentRow)

