function containsHtmlTags(str) {
	var regex = /<[^>]+>/;
	return regex.test(str);
}