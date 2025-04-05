from score_analyzer.score_reader import data_to_notes

chorales_data = open("chorales/test.mscx", "r").readlines()

print(data_to_notes(chorales_data))
