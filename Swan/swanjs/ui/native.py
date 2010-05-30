from Composite import Composite

class Body(Composite):
	
	def __init__(self):
		self.element =  native("document.documentElement.lastChild")
		self.element.proxy = self
		self.alphaIndex = "a"
		self.childCount = 0
	
class LocalActor(object):
	
	def __init__(self, arguments):
		if self.birth:
			self.birth(arguments)
			
def failure_default(status, text):
	print "Uncaught request failure code " + status

def callback(call, success, failure):
	native(
		"""failure = typeof(failure) != 'undefined' ? failure : native_failure_default;
		var sxhr = call[0];
		var body = call[1];
		var request = sxhr.request;
		var handler = function(){
			if(request.readyState==4){
				if(request.status>=200 && request.status<300){
					success.call(success.__self__, JSON.parse(request.responseText))
				}else if(request.status>=400){
					failure.call(failure.__self__, request.status, JSON.parse(request.responseText))
				}
			}
		};
		request.onreadystatechange = handler;
		sxhr.open().setHeader('Content-type','application/json').send(JSON.stringify(body))"""
	)
	