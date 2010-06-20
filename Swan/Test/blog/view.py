from Swan.swanjs.ui.native import body, callback, LocalActor
from Swan.swanjs.ui.Composite import Container, List, P
from Swan.swanjs.ui.Input import Form, TextBox, TextArea, Button, SubmitButton
		
class ControllerActor(LocalActor):

	def birth(self, username):
		print "Initialising RequestActor for " + username
		self.username = username
		self.timeline = Timelines()
		self.followers = Followers()
		self.statuses = Statuses()
		self.users = Users()

	def submit_status(self, status, success, failure):
		print "Submitting new status"
		callback(self.statuses.post(self.username, status), success, failure)

	def loadFollowers(self, layout):
		print "Loading followers for " + self.username
		callback(self.followers.get_followers(self.username), layout)

	def loadFollowing(self, layout):
		print "Loading followers for " + self.username
		callback(self.followers.get(self.username), layout)

	def loadUsers(self, layout):
		print "Loading all users"
		callback(self.users.get(), layout)
		
	def getTimeline(self, layout):
		print "Getting timeline for " + self.username
		callback(self.timeline.get(self.username), layout)
		
	def getStatuses(self, layout):
		print "Getting statuses for " + self.username
		callback(self.statuses.get(self.username), layout)

		def failed(self, status):
			print status

		class PostsList(List):

			def __init__(self, control):
				super(PostsList, self).__init__()
				self.posts = Posts()
				callback(Posts().get(), self.displayPosts, failed)

			def displayPosts(self,ps):
				for p in ps:
					self.addItem(Post(p))

		class Post(P):

			def __init__(self, post):
				super(Post, self).__init__()
				self.post = post
				self.showing = False;
				self.title = P(post.title).on_click(self.show)
				self.content = P(post.content).setVisible(False)
				self.timestamp = P(post.timestamp).setVisible(False)
				self.add(self.title,self.content,self.timestamp)

			def show(self):
				self.showing = not self.showing
				self.content.setVisible(self.showing)
				self.timestamp.setVisible(self.showing)
				if self.comments:
					self.comments.setVisible(self.showing)
				else:
					self.comments = CommentsList(self.post.id)

		class CommentsList(List):

			def __init__(self, id):
				super(CommentsList, self).__init__()
				callback(Posts().get_comments(id), self.displayComments, failed)

			def displayComments(self,cs):
				for c in cs:
					self.add(P(c.name),P(c.comment),P(c.timestamp))

		def launch():
			body.add(PostsList())