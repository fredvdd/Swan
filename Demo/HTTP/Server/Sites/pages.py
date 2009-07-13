NDUNN = """<body>
<span style="font-size:large">Neil Graham Dunn</span>

<div id="content">

<div id="twitter">
<span id="twitter_status"></span> <span id="twitter_time"></span>
(<a href="http://twitter.com/ndunn">via twitter</a>)
</div>

<p>
Welcome to my homepage. I'm 22, I live in East London and I spend my
days at Imperial College London studying computer science.
</p>

<p>
<a href="/about">about</a>
<a href="mailto:ndunn@ndunn.com">email me</a>
<a href="http://www.amazon.co.uk/gp/registry/wishlist/4WO0VD4HKQI9/">
buy me books</a>
<a href="blocks">blocks</a>
</p>

<div id="latest">
Latest blog: <a href="/2007/gtypist">gtypist</a>
</div>

<p>
I blog:
<a href="/2006/">2006</a>
<a href="/2007/">2007</a>
<a href="/ndunn.atom">Subscribe to my atom feed</a>.
</p>
</div>
</body>"""

MONITOR_TEMPLATE = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en-AU">
  <head>
    <meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
    <title>Network Monitor</title>
<style>

body {
  font-family: verdana, helvetica, arial, sans-serif;
  font-size: 73%%;  /* Enables font size scaling in MSIE */
  margin: 0;
  padding: 0;
}

html > body {
  font-size: 9pt;
}

ol {
  margin: 1em 0 1.5em 0;
  padding: 0;
}

ul {
  list-style-type: square;
  margin: 1em 0 1.5em 0;
  padding: 0;
}

dl {
  margin: 1em 0 0.5em 0;
  padding: 0;
}

ul li {
  line-height: 1.5em;
  margin: 1.25ex 0 0 1.5em;
  padding: 0;
}

ol li {
  line-height: 1.5em;
  margin: 1.25ex 0 0 2em;
  padding: 0;
}

dt {
  font-weight: bold;
  margin: 0;
  padding: 0 0 1ex 0;
}

dd {
  line-height: 1.75em;
  margin: 0 0 1.5em 1.5em;
  padding: 0;
}

.doNotDisplay {
  display: none !important;
}

.smallCaps {
  font-size: 117%%;
  font-variant: small-caps;
}

.midHeader {
  color: white;
  margin: 0;
  padding: 0.26ex 10px;
}

.headerTitle {
  font-size: 300%%;
  margin: 0;
  padding: 0;
}

.headerSubTitle {
  font-size: 151%%;
  font-weight: normal;
  font-style: italic;
  margin: 0 0 1ex 0;
  padding: 0;
}

.headerLinks {
  text-align: right;
  margin: 0;
  padding: 0 0 2ex 0;
  position: absolute;
  right: 1.5em;
  top: 3.5em;
}

.headerLinks a {
  color: white;
  background-color: transparent;
  text-decoration: none;
  margin: 0;
  padding: 0 0 0.5ex 0;
  display: block;
}

.headerLinks a:hover {
  color: rgb(195,196,210);
  background-color: transparent;
  text-decoration: underline;
}

.subHeader {
  color: white;
  margin: 0;
  padding: 0.5ex 10px;
}

.subHeader a, .subHeader .highlight {
  color: white;
  background-color: transparent;
  font-size: 110%%;
  font-weight: bold;
  text-decoration: none;
  margin: 0;
  padding: 0 0.25ex 0 0;
}

.subHeader a:hover, .subHeader .highlight {
  color: rgb(255,204,0);
  background-color: transparent;
  text-decoration: none;
}
  a {
        font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
        font-size: 200%%;
        margin: 0;
        padding: 0;
      }

#main-copy {
  margin: 0;
  padding: 0.5em 10px;
  clear: left;
}

#main-copy h1 {
  color: rgb(117,144,174);
  background-color: transparent;
  font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
  font-size: 200%%;
  margin: 0;
  padding: 0;
}

#main-copy h2 {
  color: rgb(61,92,122);
  background-color: transparent;
  font-family: "trebuchet ms", verdana, helvetica, arial, sans-serif;
  font-weight: normal;
  font-size: 151%%;
  margin: 0;
  padding: 1ex 0 0 0;
}

#main-copy p {
  line-height: 1.75em;
  margin: 1em 0 1.5em 0;
  padding: 0;
}

.rowOfBoxes {
  clear: both;
}

.fullWidth {
  margin: 1em 0;
  float: left;
  border-left: 1px solid rgb(204,204,204);
  text-align: justify;
  width: 96%%;
  padding: 0 1.2em;
  border-left: none;
}

.filler {  /* use with an empty <p> element to add padding to the end of a text box */
  border: 1px solid white;
}
 
.noBorderOnLeft {
  border-left: none;
}

.dividingBorderAbove {
  border-top: 1px solid rgb(204,204,204);
}

</style>
  </head>

  <body>
     <div id="header">
      <div class="midHeader" bgcolor="rgb(61,92,122)">
        <h1 class="headerTitle">Network Monitor</h1>

        <div class="headerSubTitle" title="Sub Header">
          Probing hosts with Actors
        </div>
        <br class="doNotDisplay doNotPrint" />
      </div>
      
       <div class="subHeader" bgcolor="rgb(117,144,174)">
        <span class="doNotDisplay">Navigation:</span>
        <a href="http://www.monitor.com/">Return to host list</a>
      </div>
    </div>
    <div id="main-copy">
       %s
    </div>
  </body>
</html>"""