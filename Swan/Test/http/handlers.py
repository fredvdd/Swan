from Swan.server import Handler, ExternalHandler

class FlickrHandler(ExternalHandler):
	bindings = {'default':'/flickr/`user`'}
	
	def get(self, user):
		print "Request for " + user
		conn = self.get_connection('api.flickr.com')
		print conn, type(conn)
		conn.get('/services/rest/?method=flickr.people.getPublicPhotos&api_key=745bf5cec0e4c9a5e9d225ce015b2e84&username=' + user)
		print "Request sent"
		resp = conn.getresponse().read()
		print resp
		
#GET /flickr/dontmindme HTTP/1.1