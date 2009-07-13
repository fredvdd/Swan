import gtkhtml2
from Actors import native
class HtmlView(gtkhtml2.View):
  """I am a simple HtmlViewer class"""
  
  def __init__(self, actor):
    gtkhtml2.View.__init__(self)
    self.actor = actor

  def display_html(self, html):
    """Does exactly what it says on the tin - 
       pass in HTML then HTML is displayed"""
    doc = gtkhtml2.Document()
    doc.clear()
    doc.open_stream("text/html")
    doc.write_stream(html)
    doc.close_stream()
    doc.connect('link_clicked', self.link_clicked)
    self.set_document(doc)
   
    
  def link_clicked(self, doc, link):
    """Internal GTK callback method"""
    # Inform the HtmlView actor that a link has been 
    # clicked
    native.send(self.actor, 'link_clicked', link)