MALFORMED_MESSAGE = """
 <p>The URL entered was not a valid URL.  The following are examples of valid URLs:
     <ul bgcolor="rgb(239,239,239)">
       <li>http://www.example.com</li>
       <li>http://www.example.com/somepage.html</li>
     </ul>
   </p>
"""

PAGE_NOT_FOUND_MESSAGE = """
 <p>The page requested was not found on the server.
 </p>
"""

BAD_HOST_MESSAGE = """
 <p>The host could not be found.
 </p>
"""

ERROR_TEMPLATE = """
  <html>
  <head>
    <style>
      h1 {
        font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
        font-size: 300%%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div bgcolor="red" color="white">
      <h1>%s</h1>
    </div>
   <div bgcolor="rgb(239,239,239)" >
   %s
  </div>
  </body>
</html>
"""


SPLASHSCREEN = """
<html>
<head>
  <style>
    h1 {
        font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
        font-size: 300%;
        margin: 0;
        padding: 0;
      }
       a {
        font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
        font-size: 300%;
        margin: 0;
        padding: 0;
      }
      
     p {
       line-height: 1.75em;
       margin: 1em 0 1.5em 0;
       padding: 0;
     }
    </style>
  </head>
  <body>
    <div bgcolor="blue" color="white">
      <h1>Nosey Badger Webbrowser</h1>
    </div>
    <div bgcolor="rgb(239,239,239)">
      <p>Welcome to the Noisey Badger Webbrowser.  Current pages include:</p>
    
           <p>A tool for <a href="http://www.monitor.com">probing</a> hosts.</p>
           <p>Going mobile?  Why not <a href="meta:migrate">Move</a> hosts?</p>
           <p>Neil Dunn's <a href="http://www.ndunn.com">Weblog</a></p>
    </div>
  </body>
</html>
"""

MIGRATION_TEMPLATE = """
  <html>
  <head>
    <style>
     a {
        font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
        font-size: 200%%;
        margin: 0;
        padding: 0;
      }
      h1 {
        font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
        font-size: 300%%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div bgcolor="blue" color="white">
      <h1>Moving computers?</h1>
    </div>
    <div bgcolor="rgb(239,239,239)">
      %s
    </div>
  </body>
</html>
"""

MALFORMED_URL = ERROR_TEMPLATE % ("Malformed URL", MALFORMED_MESSAGE)
PAGE_NOT_FOUND = ERROR_TEMPLATE % ("404 Page not found", PAGE_NOT_FOUND_MESSAGE)
BAD_HOST = ERROR_TEMPLATE % ("Bad hostname", BAD_HOST_MESSAGE)
