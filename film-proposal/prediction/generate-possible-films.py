# description: generate all possible combinations of films given our predictive features
# author: Paul Prae
# since: 4/18/2015
# tested with Python 3.3 on Windows 8.1 64-bit. runs pretty quick for so many 'for loops'!

import csv

if __name__=="__main__":

	outputFile = './data/possible_films.csv'
	filmWriter = csv.writer(open(outputFile, 'w', newline=''))

	# TODO: make sure the order of the for loops are the same as the order of the headers
	# Step 1: Setup column headers
	rowHeaders = ['Budget', 'MPAA_Rating']

	releaseSeasons = [
		'Release_in_Winter',
		'Release_in_Spring',
		'Release_in_Summer',
		'Release_in_Fall',
		'Release_in_Holiday'
	]

	actors = [
		'Actor_Morgan_Freeman',
		'Actor_Dennis_Hopper',
		'Actor_Henry_Fonda',
		'Actor_Bruce_Willis',
		'Actor_Samuel_L__Jackson',
		'Actor_Robert_De_Niro',
		'Actor_Burt_Lancaster',
		'Actor_Donald_Sutherland',
		'Actor_Christopher_Lee',
		'Actor_John_Wayne',
		'Actor_Keanu_Reeves',
		'Actor_Nick_Nolte',
		'Actor_Nicolas_Cage',
		'Actor_Gene_Hackman',
		'Actor_Michael_Caine',
		'Actor_Sean_Connery',
		'Actor_Oliver_Hardy',
		'Actor_Stan_Laurel',
		'Actor_Robert_Duvall',
		'Actor_Susan_Sarandon',
		'Actor_Jack_Nicholson',
		'Actor_Robert_Downey_Jr_',
		'Actor_Christopher_Walken',
		'Actor_Willem_Dafoe',
		'Actor_James_Stewart',
		'Actor_Dustin_Hoffman',
		'Actor_Robin_Williams',
		'Actor_John_Goodman',
		'Actor_Dennis_Quaid',
		'Actor_Harvey_Keitel'
	]

	directors = [
		'Director_Blake_Edwards',
		'Director_Sidney_Lumet',
		'Director_Steven_Spielberg',
		'Director_Spike_Lee',
		'Director_John_Ford',
		'Director_Robert_Altman',
		'Director_Charlie_Chaplin',
		'Director_Vincente_Minnelli',
		'Director_Woody_Allen',
		'Director_Clint_Eastwood',
		'Director_Martin_Scorsese',
		'Director_Ingmar_Bergman',
		'Director_Howard_Hawks',
		'Director_John_Huston',
		'Director_Raoul_Walsh',
		'Director_Chuck_Jones',
		'Director_Werner_Herzog',
		'Director_Fritz_Lang',
		'Director_Steven_Soderbergh',
		'Director_Michael_Curtiz',
		'Director_Francis_Ford_Coppola',
		'Director_Roger_Corman',
		'Director_Alfred_Hitchcock',
		'Director_Friz_Freleng',
		'Director_Anthony_Mann',
		'Director_Norman_Taurog',
		'Director_Akira_Kurosawa'
	]

	genres = [
		'Genre_comedy',
		'Genre_drama',
		'Genre_romantic',
		'Genre_science_fiction',
		'Genre_crime',
		'Genre_action',
		'Genre_thriller',
		'Genre_horror',
		'Genre_animated'
	]

	rowHeaders.extend(releaseSeasons)
	rowHeaders.extend(actors)
	rowHeaders.extend(directors)
	rowHeaders.extend(genres)
	filmWriter.writerow(rowHeaders)

	# Step 2: Create all possible values for each column.
	# Note: Some will be sparse arrays of booleans. The '1' will indicate the column for that mapped variable.
	budgetValues = [100000000,200000000]
	MPAARatingValues = ['PG-13', 'R', 'G', 'PG', 'NC-17']

	releaseSeasonValues = {
		'Release_in_Winter':	[1,0,0,0,0],
		'Release_in_Spring':	[0,1,0,0,0],
		'Release_in_Summer':	[0,0,1,0,0],
		'Release_in_Fall':		[0,0,0,1,0],
		'Release_in_Holiday': 	[0,0,0,0,1]
	}

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

	directorValues = {
		'Director_Blake_Edwards':			[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Sidney_Lumet':			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Steven_Spielberg':		[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Spike_Lee':				[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_John_Ford': 				[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Robert_Altman': 			[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Charlie_Chaplin': 		[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Vincente_Minnelli': 		[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Woody_Allen': 			[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Clint_Eastwood': 			[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Martin_Scorsese': 		[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Ingmar_Bergman': 			[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Howard_Hawks': 			[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_John_Huston': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Raoul_Walsh': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Chuck_Jones': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
		'Director_Werner_Herzog': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
		'Director_Fritz_Lang': 				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
		'Director_Steven_Soderbergh': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
		'Director_Michael_Curtiz': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
		'Director_Francis_Ford_Coppola':	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
		'Director_Roger_Corman': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
		'Director_Alfred_Hitchcock': 		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
		'Director_Friz_Freleng':			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		'Director_Anthony_Mann': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
		'Director_Norman_Taurog': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
		'Director_Akira_Kurosawa': 			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
	}

	genreValues = {
		'Genre_comedy':			[1,0,0,0,0,0,0,0,0],
		'Genre_drama':			[0,1,0,0,0,0,0,0,0],
		'Genre_romantic':		[0,0,1,0,0,0,0,0,0],
		'Genre_science_fiction':[0,0,0,1,0,0,0,0,0],
		'Genre_crime': 			[0,0,0,0,1,0,0,0,0],
		'Genre_action': 		[0,0,0,0,0,1,0,0,0],
		'Genre_thriller': 		[0,0,0,0,0,0,1,0,0],
		'Genre_horror': 		[0,0,0,0,0,0,0,1,0],
		'Genre_animated': 		[0,0,0,0,0,0,0,0,1]
	}

	count = 0
	# Step 3: Initiate the for loop over the column values. This should generate 420,000 unique possibilities. 
	# TODO: make sure the order of the for loops are the same as the order of the headers
	for budget in budgetValues: # 2 values creates 2 possibilities
		for MPAARating in MPAARatingValues: # 5 more values creates 10 more possibilities
			for releaseSeason in releaseSeasons: # 5 more values creates 50 more possibilities
				for actor in actors: # 30 more values creates 1500 more possibilities
					for director in directors: # 27 more values creates 40500 more possibilities
						for genre in genres: # 9 more values creates 364500 more possibilities
						
							# Step 4: Write the unique possibility (combination of values) out as a row.
							# Note: this all should only be on the inner most loop
							count += 1
							print(count)

							currentRow = []
							currentRow.append(budget)
							currentRow.append(MPAARating)
							currentRow.extend(releaseSeasonValues[releaseSeason])
							currentRow.extend(actorValues[actor])
							currentRow.extend(directorValues[director])
							currentRow.extend(genreValues[genre])
														
							filmWriter.writerow(currentRow)

