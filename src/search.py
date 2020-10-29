def search(text, query):
	# Get text tokens
	tokens = text.lower().split()

	# Scoring functions
	score = lambda x: len(set(tokens).intersection(x.lower().split()))

	# Filter query by score
	filtered = sorted(filter(score, query), key=score, reverse=True)

	return filtered

