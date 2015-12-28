// Copyright 2008, 2009 Hannes Hochreiner
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.

// Set onload event handler.
window.onload = jessyInkInit;

// Creating a namespace dictionary. The standard Inkscape namespaces are taken from inkex.py.
var NSS = new Object();
NSS['sodipodi']='http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd';
NSS['cc']='http://web.resource.org/cc/';
NSS['svg']='http://www.w3.org/2000/svg';
NSS['dc']='http://purl.org/dc/elements/1.1/';
NSS['rdf']='http://www.w3.org/1999/02/22-rdf-syntax-ns#';
NSS['inkscape']='http://www.inkscape.org/namespaces/inkscape';
NSS['xlink']='http://www.w3.org/1999/xlink';
NSS['xml']='http://www.w3.org/XML/1998/namespace';
NSS['jessyink']='https://launchpad.net/jessyink';

// Keycodes.
var MINUS_KEY = 109;
var EQUAL_KEY = 107; //on UK keyboards, this the plus key is equal + shift
var EQUAL_KEY_OPERA = 61;
var MINUS_KEY_SAFARI = 189;
var EQUAL_KEY_SAFARI = 187;
var SPACE_KEY = 32;
var PAGE_UP_KEY = 33;
var PAGE_DOWN_KEY = 34;
var END_KEY = 35;
var HOME_KEY = 36;
var LEFT_KEY = 37;
var UP_KEY = 38;
var RIGHT_KEY = 39;
var DOWN_KEY = 40;
var INDEX_KEY = 73; // "i"
var ENTER_KEY = 13;

// Presentation modes.
var SLIDE_MODE = 1;
var INDEX_MODE = 2;

// Parameters.
var ROOT_NODE = document.getElementsByTagNameNS(NSS["svg"], "svg")[0];
var HEIGHT = parseFloat(ROOT_NODE.getAttribute("height"));
var WIDTH = parseFloat(ROOT_NODE.getAttribute("width"));
var INDEX_COLUMNS = 3;
var INDEX_OFFSET = 0;
var STATE_START = -1;
var STATE_END = -2;
var slides = new Array();
var TITLE_NODE;

// Initialisation.
var currentMode = SLIDE_MODE;
var activeSlide = 0;
var activeEffect = 0;
var timeStep = 30; // 40 ms equal 25 frames per second.
var lastFrameTime = null;
var processingEffect = false;
var transCounter = 0;
var effectArray = 0;
var defaultTransitionInDict = new Object();
defaultTransitionInDict["name"] = "appear";
var defaultTransitionOutDict = new Object();
defaultTransitionOutDict["name"] = "appear";
var jessyInkInitialised = false;

/** Initialisation function.
 *  The whole presentation is set-up in this function.
 */
function jessyInkInit()
{
	// Make sure we only execute this code once. Double execution can occur if the onload event handler is set
	// in the main svg tag as well (as was recommended in earlier versions). Executing this function twice does
	// not lead to any problems, but it takes more time.
	if (jessyInkInitialised)
		return;

        // Creating the title node.
        TITLE_NODE = document.createElementNS(NSS["svg"], "title");
        TITLE_NODE.appendChild(document.createTextNode(""));
        ROOT_NODE.appendChild(TITLE_NODE);

	// Making the presentation scaleable.
	ROOT_NODE.setAttribute("width", "100%");
	ROOT_NODE.setAttribute("height", "100%");
	ROOT_NODE.setAttribute("viewBox", "0 0 "+WIDTH+" "+HEIGHT);

	// Setting the background color.
	var namedViews = document.getElementsByTagNameNS(NSS["sodipodi"], "namedview");
		
	for (var counter = 0; counter < namedViews.length; counter++)
	{
		if (namedViews[counter].hasAttribute("id") && namedViews[counter].hasAttribute("pagecolor"))
		{
			if (namedViews[counter].getAttribute("id") == "base")
			{
				var newAttribute = "background-color:" + namedViews[counter].getAttribute("pagecolor") + ";";

				if (ROOT_NODE.hasAttribute("style"))
					newAttribute += ROOT_NODE.getAttribute("style");

				ROOT_NODE.setAttribute("style", newAttribute);
			}
		}
	}

	// Defining clip-path.
	var defsNodes = document.getElementsByTagNameNS(NSS["svg"], "defs");
	
	if (defsNodes.length > 0)
	{
		var rectNode = document.createElementNS(NSS["svg"], "rect");
		var clipPath = document.createElementNS(NSS["svg"], "clipPath");
		
		rectNode.setAttribute("x", 0);
		rectNode.setAttribute("y", 0);
		rectNode.setAttribute("width", WIDTH);
		rectNode.setAttribute("height", HEIGHT);

		clipPath.setAttribute("id", "jessyInkSlideClipPath");
		clipPath.setAttribute("clipPathUnits", "userSpaceOnUse");

		clipPath.appendChild(rectNode);
		defsNodes[0].appendChild(clipPath);
	}

	// Making a list of the slide and finding the master slide.
	var nodes = document.getElementsByTagNameNS(NSS["svg"], "g");
	var tempSlides = new Array();
	var masterSlide = null;

	for (var counter = 0; counter < nodes.length; counter++)
	{
		if (nodes[counter].getAttributeNS(NSS["inkscape"], "groupmode") && (nodes[counter].getAttributeNS(NSS["inkscape"], "groupmode") == "layer"))
		{
			if (nodes[counter].getAttributeNS(NSS["inkscape"], "label") && nodes[counter].getAttributeNS(NSS["jessyink"], "masterSlide") == "masterSlide")
				masterSlide = nodes[counter];
			else
				tempSlides.push(nodes[counter].getAttribute("id"));
		}
	}

	// Removing master slide from main tree and setting default transitions.
	if (masterSlide)
	{
		masterSlide.parentNode.removeChild(masterSlide);
		masterSlide.style.display = "inherit";

		if (masterSlide.hasAttributeNS(NSS["jessyink"], "transitionIn"))
			defaultTransitionInDict = propStrToDict(masterSlide.getAttributeNS(NSS["jessyink"], "transitionIn"));

		if (masterSlide.hasAttributeNS(NSS["jessyink"], "transitionOut"))
			defaultTransitionOutDict = propStrToDict(masterSlide.getAttributeNS(NSS["jessyink"], "transitionOut"));
	}

	// Set start slide.
	var paramString = window.location.hash;

	paramString = paramString.substr(1, paramString.length);
	
	if (!isNaN(parseInt(paramString)))
			activeSlide = parseInt(paramString) - 1;

	if (activeSlide < 0)
		activeSlide = 0;
	else if (activeSlide >= tempSlides.length)
		activeSlide = tempSlides.length - 1;

	// Gathering all the information about the transitions and effects of the slides, set the background
	// from the master slide and substitute the auto-texts.
	for (var counter = 0; counter < tempSlides.length; counter++)
	{
		var node = document.getElementById(tempSlides[counter]);
		slides[counter] = new Object();

		// Set node.
		slides[counter]["element"] = node;

                // Set name.
                slides[counter]["label"] = node.getAttributeNS(NSS["inkscape"], "label");

		// Set build in transition.
		slides[counter]["transitionIn"] = new Object();

		var dict;

		if (node.hasAttributeNS(NSS["jessyink"], "transitionIn"))
			dict = propStrToDict(node.getAttributeNS(NSS["jessyink"], "transitionIn"));
		else
			dict = defaultTransitionInDict;

		slides[counter]["transitionIn"]["name"] = dict["name"];
		slides[counter]["transitionIn"]["options"] = new Object();

		for (key in dict)
			if (key != "name")
				slides[counter]["transitionIn"]["options"][key] = dict[key];

		// Set build out transition.
		slides[counter]["transitionOut"] = new Object();

		if (node.hasAttributeNS(NSS["jessyink"], "transitionOut"))
			dict = propStrToDict(node.getAttributeNS(NSS["jessyink"], "transitionOut"));
		else
			dict = defaultTransitionOutDict;

		slides[counter]["transitionOut"]["name"] = dict["name"];
		slides[counter]["transitionOut"]["options"] = new Object();

		for (key in dict)
			if (key != "name")
				slides[counter]["transitionOut"]["options"][key] = dict[key];

		// Copy master slide content.
		if (masterSlide)
		{
			var clonedNode = suffixNodeIds(masterSlide.cloneNode(true), "_" + counter);
			
			node.insertBefore(clonedNode, node.firstChild);
		}

		// Setting clip path.
		node.setAttribute("clip-path", "url(#jessyInkSlideClipPath)");

		// Substitute auto texts.
		substituteAutoTexts(node, node.getAttributeNS(NSS["inkscape"], "label"), counter + 1, tempSlides.length);

		// Set visibility for initial state.
		if (counter == activeSlide)
		{
			node.style.display = "inherit";
			node.setAttribute("opacity",1);
		}
		else
		{
			node.style.display = "none";
			node.setAttribute("opacity",0);
		}

		// Set effects.
		var tempEffects = new Array();
		var groups = new Object();

		for (var IOCounter = 0; IOCounter <= 1; IOCounter++)
		{
			var propName = "";
			var dir = 0;

			if (IOCounter == 0)
			{
				propName = "effectIn";
				dir = 1;
			}
			else if (IOCounter == 1)
			{
				propName = "effectOut";
				dir = -1;
			}

			var effects = getElementsByPropertyNS(node, NSS["jessyink"], propName);

			for (var effectCounter = 0; effectCounter < effects.length; effectCounter++)
			{
				var element = document.getElementById(effects[effectCounter]);
				var dict = propStrToDict(element.getAttributeNS(NSS["jessyink"], propName));

				// Put every element that has an effect associated with it, into its own group.
				// Unless of course, we already put it into its own group.
				if (!(groups[element.id]))
				{
					var newGroup = document.createElementNS(NSS["svg"], "g");
					
					element.parentNode.insertBefore(newGroup, element);
					newGroup.appendChild(element.parentNode.removeChild(element));
					groups[element.id] = newGroup;
				}

				var effectDict = new Object();

				effectDict["effect"] = dict["name"];
				effectDict["dir"] = dir;
				effectDict["element"] = groups[element.id];

				for (var option in dict)
				{
					if ((option != "name") && (option != "order"))
					{
						if (!effectDict["options"])
							effectDict["options"] = new Object();

						effectDict["options"][option] = dict[option];
					}
				}

				if (!tempEffects[dict["order"]])
					tempEffects[dict["order"]] = new Array();

				tempEffects[dict["order"]][tempEffects[dict["order"]].length] = effectDict;
			}
		}

		if (tempEffects.length > 0)
		{
			slides[counter]["effects"] = new Array();
			for (var effectCounter = 0; effectCounter < tempEffects.length; effectCounter++)
			{
				if (tempEffects[effectCounter])
					slides[counter]["effects"][slides[counter]["effects"].length] = tempEffects[effectCounter];
			}
		}
	}
	
	setSlideToState(activeSlide, STATE_START);
	setActiveSlideTitle();

	jessyInkInitialised = true;
}

/** Convenience function to set the title.
 *	This function displays the title of the active slide
 */
function setActiveSlideTitle()
{
	TITLE_NODE.firstChild.data = slides[activeSlide]["label"];
}

/** Function to subtitute the auto-texts.
 *
 *  @param node the node
 *  @param slideName name of the slide the node is on
 *  @param slideNumber number of the slide the node is on
 *  @param numberOfSlides number of slides in the presentation
 */
function substituteAutoTexts(node, slideName, slideNumber, numberOfSlides)
{
	var texts = node.getElementsByTagNameNS(NSS["svg"], "tspan");

	for (var textCounter = 0; textCounter < texts.length; textCounter++)
	{
		if (texts[textCounter].getAttributeNS(NSS["jessyink"], "autoText") == "slideNumber")
			texts[textCounter].firstChild.nodeValue = slideNumber;
		else if (texts[textCounter].getAttributeNS(NSS["jessyink"], "autoText") == "numberOfSlides")
			texts[textCounter].firstChild.nodeValue = numberOfSlides;
		else if (texts[textCounter].getAttributeNS(NSS["jessyink"], "autoText") == "slideTitle")
			texts[textCounter].firstChild.nodeValue = slideName;
	}
}

/** Convenience function to get an element depending on whether it has a property with a particular name.
 *	This function emulates some dearly missed XPath functionality.
 *
 *  @param node the node
 *  @param namespace namespace of the attribute
 *  @param name attribute name
 */
function getElementsByPropertyNS(node, namespace, name)
{
	var elems = new Array();

	if (node.getAttributeNS(namespace, name))
		elems.push(node.getAttribute("id"));

	for (var counter = 0; counter < node.childNodes.length; counter++)
	{
		if (node.childNodes[counter].nodeType == 1)
			elems = elems.concat(getElementsByPropertyNS(node.childNodes[counter], namespace, name));
	}

	return elems;
}

/** Function to dispatch the next effect, if there is none left, change the slide.
 *
 *  @param dir direction of the change (1 = forwards, -1 = backwards)
 */
function dispatchEffects(dir)
{
	if (slides[activeSlide]["effects"] && (((dir == 1) && (activeEffect < slides[activeSlide]["effects"].length)) || ((dir == -1) && (activeEffect > 0))))
	{
		processingEffect = true;

		if (dir == 1)
		{
			effectArray = slides[activeSlide]["effects"][activeEffect];
			activeEffect += dir;
		}
		else if (dir == -1)
		{
			activeEffect += dir;
			effectArray = slides[activeSlide]["effects"][activeEffect];
		}

		transCounter = 0;
		startTime = (new Date()).getTime();
		lastFrameTime = startTime;
		effect(dir);
	}
	else if (((dir == 1) && (activeSlide < (slides.length - 1))) || (((dir == -1) && (activeSlide > 0))))
	{
		changeSlide(dir);
	}
}

/** Function to skip effects and directly either put the slide into start or end state or change slides.
 *
 *  @param dir direction of the change (1 = forwards, -1 = backwards)
 */
function skipEffects(dir)
{
	if (slides[activeSlide]["effects"] && (((dir == 1) && (activeEffect < slides[activeSlide]["effects"].length)) || ((dir == -1) && (activeEffect > 0))))
	{
		processingEffect = true;

		if (slides[activeSlide]["effects"] && (dir == 1))
			activeEffect = slides[activeSlide]["effects"].length;
		else
			activeEffect = 0;

		if (dir == 1)
			setSlideToState(activeSlide, STATE_END);
		else
			setSlideToState(activeSlide, STATE_START);

		processingEffect = false;
	}
	else if (((dir == 1) && (activeSlide < (slides.length - 1))) || (((dir == -1) && (activeSlide > 0))))
	{
		changeSlide(dir);
	}
}

/** Function to change between slides.
 *
 *  @param dir direction (1 = forwards, -1 = backwards)
 */
function changeSlide(dir)
{
	processingEffect = true;
	effectArray = new Array();

	effectArray[0] = new Object();
	if (dir == 1)
	{
		effectArray[0]["effect"] = slides[activeSlide]["transitionOut"]["name"];
		effectArray[0]["options"] = slides[activeSlide]["transitionOut"]["options"];
		effectArray[0]["dir"] = -1;
	}
	else if (dir == -1)
	{
		effectArray[0]["effect"] = slides[activeSlide]["transitionIn"]["name"];
		effectArray[0]["options"] = slides[activeSlide]["transitionIn"]["options"];
		effectArray[0]["dir"] = 1;
	}
	effectArray[0]["element"] = slides[activeSlide]["element"];

	activeSlide += dir;
	window.location.hash = activeSlide + 1;

	effectArray[1] = new Object();
	if (dir == 1)
	{
		effectArray[1]["effect"] = slides[activeSlide]["transitionIn"]["name"];
		effectArray[1]["options"] = slides[activeSlide]["transitionIn"]["options"];
		effectArray[1]["dir"] = 1;
	}
	else if (dir == -1)
	{
		effectArray[1]["effect"] = slides[activeSlide]["transitionOut"]["name"];
		effectArray[1]["options"] = slides[activeSlide]["transitionOut"]["options"];
		effectArray[1]["dir"] = -1;
	}
	effectArray[1]["element"] = slides[activeSlide]["element"];

	if (slides[activeSlide]["effects"] && (dir == -1))
		activeEffect = slides[activeSlide]["effects"].length;
	else
		activeEffect = 0;

	if (dir == -1)
		setSlideToState(activeSlide, STATE_END);
	else
		setSlideToState(activeSlide, STATE_START);

	setActiveSlideTitle();

	transCounter = 0;
	startTime = (new Date()).getTime();
	lastFrameTime = startTime;
	effect(dir);
}

/** Function to toggle between index and slide mode.
 */
function toggleSlideIndex()
{
	if (currentMode == SLIDE_MODE)
	{
		INDEX_OFFSET = Math.min(Math.floor(activeSlide / INDEX_COLUMNS) * INDEX_COLUMNS, Math.floor((slides.length - 1) / INDEX_COLUMNS - INDEX_COLUMNS + 1) * INDEX_COLUMNS);
		displayIndex(INDEX_OFFSET);
		slides[activeSlide]["element"].setAttribute("opacity",1);
		currentMode = INDEX_MODE;
	}
	else if (currentMode == INDEX_MODE)
	{
		for (var counter = 0; counter < slides.length; counter++)
		{
			slides[counter]["element"].setAttribute("transform","scale(1)");

			if (counter == activeSlide)
			{
				slides[counter]["element"].style.display = "inherit";
				slides[counter]["element"].setAttribute("opacity",1);
				activeEffect = 0;
			}
			else
			{
				slides[counter]["element"].setAttribute("opacity",0);
				slides[counter]["element"].style.display = "none";
			}
		}
		currentMode = SLIDE_MODE;
		setSlideToState(activeSlide, STATE_START);
	}
}

/** Function to run an effect.
 *
 *  @param dir direction in which to play the effect (1 = forwards, -1 = backwards)
 */
function effect(dir)
{
	var done = true;

	for (var counter = 0; counter < effectArray.length; counter++)
	{
		if (effectArray[counter]["effect"] == "fade")
			done &= fade(parseInt(effectArray[counter]["dir"]) * dir, effectArray[counter]["element"], transCounter, effectArray[counter]["options"]);
		else if (effectArray[counter]["effect"] == "appear")
			done &= appear(parseInt(effectArray[counter]["dir"]) * dir, effectArray[counter]["element"], transCounter, effectArray[counter]["options"]);
		else if (effectArray[counter]["effect"] == "pop")
			done &= pop(parseInt(effectArray[counter]["dir"]) * dir, effectArray[counter]["element"], transCounter, effectArray[counter]["options"]);
	}

	if (!done)
	{
		var currentTime = (new Date()).getTime();

		transCounter = currentTime - startTime;
		var timeDiff = timeStep - (currentTime - lastFrameTime);
		lastFrameTime = currentTime;

		if (timeDiff <= 0)
			timeDiff = 1;

		window.setTimeout("effect(" + dir + ")", timeDiff);
	}
	else
		processingEffect = false;
}

/** Function to display the index sheet.
 *
 *  @param offsetNumber offset number
 */
function displayIndex(offsetNumber)
{
	var offsetX = 0;
	var offsetY = 0;

	for (var counter = 0; counter < slides.length; counter++)
	{
		if ((counter < offsetNumber) || (counter > offsetNumber + INDEX_COLUMNS * INDEX_COLUMNS))
		{
			slides[counter]["element"].setAttribute("opacity",0);
			slides[counter]["element"].style.display = "none";
		}
		else
		{
			slides[counter]["element"].setAttribute("transform","scale("+1/INDEX_COLUMNS+") translate("+offsetX+","+offsetY+")");
			slides[counter]["element"].style.display = "inherit";
			slides[counter]["element"].setAttribute("opacity",0.5);

			if ((offsetX + WIDTH) >= (WIDTH * INDEX_COLUMNS))
			{
				offsetX = 0;
				offsetY += HEIGHT;
			}
			else
				offsetX += WIDTH;
		}
		setSlideToState(counter, STATE_END);
	}
}

/** Function to set the active slide in the index view.
 *
 *  @param nbr index of the active slide
 */
function indexSetActiveSlide(nbr)
{
	if (nbr >= slides.length)
		nbr = slides.length - 1;
	else if (nbr < 0)
		nbr = 0;

	slides[activeSlide]["element"].setAttribute("opacity",0.5);
	if (nbr < INDEX_OFFSET)
		INDEX_OFFSET = Math.floor(nbr / INDEX_COLUMNS) * INDEX_COLUMNS;
	else if (nbr > (INDEX_OFFSET + INDEX_COLUMNS * INDEX_COLUMNS - 1))
		INDEX_OFFSET = (Math.floor(nbr / INDEX_COLUMNS) - INDEX_COLUMNS + 1) * INDEX_COLUMNS;

	displayIndex(INDEX_OFFSET);
	activeSlide = nbr;
	slides[activeSlide]["element"].setAttribute("opacity",1);
	window.location.hash = activeSlide + 1;

	setActiveSlideTitle();
}

/** Function to set the active slide in the index view. Position kept if possible
 *
 *  @param nbr index of the active slide
 */
function indexSetActiveSlidePageJump(nbr)
{
	if (nbr >= slides.length)
		nbr = slides.length - 1;
	else if (nbr < 0)
		nbr = 0;

	slides[activeSlide]["element"].setAttribute("opacity",0.5);
	if (nbr < INDEX_OFFSET)
	{
		INDEX_OFFSET -= INDEX_COLUMNS * INDEX_COLUMNS;
		if (INDEX_OFFSET < 0)
			INDEX_OFFSET = 0;
	}
	else if (nbr > (INDEX_OFFSET + INDEX_COLUMNS * INDEX_COLUMNS - 1))
	{
		INDEX_OFFSET += INDEX_COLUMNS * INDEX_COLUMNS;
		if (INDEX_OFFSET >= slides.length)
			INDEX_OFFSET = slides.length-1;
	}

	displayIndex(INDEX_OFFSET);
	activeSlide = nbr;
	slides[activeSlide]["element"].setAttribute("opacity",1);
	window.location.hash = activeSlide + 1;

	setActiveSlideTitle();
}

/** Event handler for key press.
 *
 *  @param e the event
 */
function keypress(e)
{
	if(!e)e=window.event;

	if (!processingEffect)
	{
		if (e.keyCode == LEFT_KEY)
		{
			if (currentMode == SLIDE_MODE)
				dispatchEffects(-1);
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlide(activeSlide - 1);
		}
		else if (e.keyCode == RIGHT_KEY || (e.keyCode == SPACE_KEY && currentMode == SLIDE_MODE))
		{
			if (currentMode == SLIDE_MODE)
				dispatchEffects(1);
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlide(activeSlide + 1);
		}
		else if (e.keyCode == UP_KEY)
		{
			if (currentMode == SLIDE_MODE)
				skipEffects(-1);
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlide(activeSlide - INDEX_COLUMNS);
		}
		else if (e.keyCode == DOWN_KEY)
		{
			if (currentMode == SLIDE_MODE)
				skipEffects(1);
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlide(activeSlide + INDEX_COLUMNS);
		}
		else if (e.keyCode == INDEX_KEY || (e.keyCode == ENTER_KEY && currentMode == INDEX_MODE))
		{
			toggleSlideIndex();
		}
		else if (e.keyCode == HOME_KEY)
		{
			if (currentMode == SLIDE_MODE)
			{
				slides[activeSlide]["element"].setAttribute("opacity",0);
				slides[activeSlide]["element"].style.display = "none";

				activeSlide = 0;
				window.location.hash = activeSlide + 1;

				setSlideToState(activeSlide, STATE_START);
				slides[activeSlide]["element"].style.display = "inherit";
				slides[activeSlide]["element"].setAttribute("opacity",1);

				activeEffect = 0;
			}
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlide(0);

			setActiveSlideTitle();
		}
		else if (e.keyCode == END_KEY)
		{
			if (currentMode == SLIDE_MODE)
			{
				slides[activeSlide]["element"].setAttribute("opacity",0);
				slides[activeSlide]["element"].style.display = "none";

				activeSlide = slides.length - 1;
				window.location.hash = activeSlide + 1;

				setSlideToState(activeSlide, STATE_END);
				slides[activeSlide]["element"].style.display = "inherit";
				slides[activeSlide]["element"].setAttribute("opacity",1);
				
				if (slides[activeSlide]["effects"])
					activeEffect = slides[activeSlide]["effects"].length;
				else
					activeEffect = 0;
			}
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlide(slides.length - 1);

			setActiveSlideTitle();
		}
		else if (e.keyCode == PAGE_UP_KEY )
		{
			if (currentMode == SLIDE_MODE)
				skipEffects(-1);
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlidePageJump(activeSlide - INDEX_COLUMNS * INDEX_COLUMNS);
		}
		else if (e.keyCode == PAGE_DOWN_KEY )
		{
			if (currentMode == SLIDE_MODE)
				skipEffects(1);
			else if (currentMode == INDEX_MODE)
				indexSetActiveSlidePageJump(activeSlide + INDEX_COLUMNS * INDEX_COLUMNS);
		}
		else if ((e.keyCode == EQUAL_KEY || e.keyCode == EQUAL_KEY_SAFARI || e.keyCode == EQUAL_KEY_OPERA) && currentMode == INDEX_MODE)
		{
			if (INDEX_COLUMNS >=3)
			{
				INDEX_COLUMNS -= 1;
				indexSetActiveSlide(activeSlide);
			}
		}
		else if ((e.keyCode == MINUS_KEY || e.keyCode == MINUS_KEY_SAFARI) && currentMode == INDEX_MODE)
		{
			if (INDEX_COLUMNS <7)
			{
				INDEX_COLUMNS += 1;
				indexSetActiveSlide(activeSlide);
			}
		}
	}
}
// Set event handler for key press.
document.onkeyup = keypress;

/** Event handler for mouse wheel events.
 *  based on http://adomas.org/javascript-mouse-wheel/
 *
 *  @param e the event
 */
function wheel(e)
{
	var delta = 0;
	if (!e)e = window.event;

	if (e.wheelDelta)
	{ // IE Opera
		delta = e.wheelDelta/120;
		//if (window.opera)
		//	delta = -delta;
	}
	else if (e.detail)
	{ // MOZ
		delta = -e.detail/3;
	}

	if (delta > 0)
	{
		if (currentMode == SLIDE_MODE)
			skipEffects(-1);
		else if (currentMode == INDEX_MODE)
			indexSetActiveSlidePageJump(activeSlide - INDEX_COLUMNS * INDEX_COLUMNS);
			//indexSetActiveSlide(activeSlide - INDEX_COLUMNS);
	}
	else if (delta < 0)
	{
		if (currentMode == SLIDE_MODE)
			skipEffects(1);
		else if (currentMode == INDEX_MODE)
			indexSetActiveSlidePageJump(activeSlide + INDEX_COLUMNS * INDEX_COLUMNS);
			//indexSetActiveSlide(activeSlide + INDEX_COLUMNS);
	}

	if (e.preventDefault)
		e.preventDefault();

	e.returnValue = false;
}

// Moz
if (window.addEventListener)
	window.addEventListener('DOMMouseScroll', wheel, false);

// IE Opera
window.onmousewheel = document.onmousewheel = wheel;


/** Event handler for mouse clicks.
 *
 *  @param e the event
 */
function mouseclick(e)
{
	if(!e)e = window.event;

	var value = 0;

	if (e.button)
		value = e.button;
	else if (e.which)
		value = e.which;

	if (value == 1)
	{
		if (currentMode == SLIDE_MODE)
		{
			dispatchEffects(1);
		}
		else if (currentMode == INDEX_MODE)
		{
			var posX = e.clientX;
			var posY = e.clientY;

			//var slide;
			window.status = "X= " + posX + " Y= " + posY;

			//indexSetActiveSlide(slide);
		}

	}
}
// Set event handler for mouse click.
document.onmousedown = mouseclick;

/** The fade effect.
 *
 *  @param dir direction the effect should be played (1 = forwards, -1 = backwards)
 *  @param element the element the effect should be applied to
 *  @param time the time that has elapsed since the beginning of the effect
 *  @param options a dictionary with additional options (e.g. length of the effect)
 */
function fade(dir, element, time, options)
{
	var length = 250;
	var fraction;

	if ((time == STATE_END) || (time == STATE_START))
		fraction = 1;
	else
	{
		if (options && options["length"])
			length = options["length"];

		fraction = time / length;
	}

	if (dir == 1)
	{
		if (fraction <= 0)
		{
			element.style.display = "none";
			element.setAttribute("opacity", 0);
		}
		else if (fraction >= 1)
		{
			element.style.display = "inherit";
			element.setAttribute("opacity", 1);
			return true;
		}
		else
		{
			element.style.display = "inherit";
			element.setAttribute("opacity", fraction);
		}
	}
	else if (dir == -1)
	{
		if (fraction <= 0)
		{
			element.style.display = "inherit";
			element.setAttribute("opacity", 1);
		}
		else if (fraction >= 1)
		{
			element.setAttribute("opacity", 0);
			element.style.display = "none";
			return true;
		}
		else
		{
			element.style.display = "inherit";
			element.setAttribute("opacity", 1 - fraction);
		}
	}
	return false;
}

/** The appear effect.
 *
 *  @param dir direction the effect should be played (1 = forwards, -1 = backwards)
 *  @param element the element the effect should be applied to
 *  @param time the time that has elapsed since the beginning of the effect
 *  @param options a dictionary with additional options (e.g. length of the effect)
 */
function appear(dir, element, time, options)
{
	if (dir == 1)
	{
		element.style.display = "inherit";
		element.setAttribute("opacity",1);
	}
	else if (dir == -1)
	{
		element.style.display = "none";
		element.setAttribute("opacity",0);
	}
	return true;
}

/** The pop effect.
 *
 *  @param dir direction the effect should be played (1 = forwards, -1 = backwards)
 *  @param element the element the effect should be applied to
 *  @param time the time that has elapsed since the beginning of the effect
 *  @param options a dictionary with additional options (e.g. length of the effect)
 */
function pop(dir, element, time, options)
{
	var length = 500;
	var fraction;

	if ((time == STATE_END) || (time == STATE_START))
		fraction = 1;
	else
	{
		if (options && options["length"])
			length = options["length"];

		fraction = time / length;
	}

	if (dir == 1)
	{
		if (fraction <= 0)
		{
			element.setAttribute("opacity", 0);
			element.setAttribute("transform", "scale(0)");
			element.style.display = "none";
		}
		else if (fraction >= 1)
		{
			element.setAttribute("opacity", 1);
			element.removeAttribute("transform");
			element.style.display = "inherit";
			return true;
		}
		else
		{
			element.style.display = "inherit";
			var opacityFraction = fraction * 3;
			if (opacityFraction > 1)
				opacityFraction = 1;
			element.setAttribute("opacity", opacityFraction);
			var offsetX = WIDTH * (1.0 - fraction) / 2.0;
			var offsetY = HEIGHT * (1.0 - fraction) / 2.0;
			element.setAttribute("transform", "translate(" + offsetX + "," + offsetY + ") scale(" + fraction + ")");
		}
	}
	else if (dir == -1)
	{
		if (fraction <= 0)
		{
			element.setAttribute("opacity", 1);
			element.setAttribute("transform", "scale(1)");
			element.style.display = "inherit";
		}
		else if (fraction >= 1)
		{
			element.setAttribute("opacity", 0);
			element.removeAttribute("transform");
			element.style.display = "none";
			return true;
		}
		else
		{
			element.setAttribute("opacity", 1 - fraction);
			element.setAttribute("transform", "scale(" + 1 - fraction + ")");
			element.style.display = "inherit";
		}
	}
	return false;
}

/** Function to set a slide either to the start or the end state.
 *  
 *  @param slide the slide to use
 *  @param state the state into which the slide should be set
 */
function setSlideToState(slide, state)
{
	if (slides[slide]["effects"])
	{	
		if (state == STATE_END)
		{
			for (var counter = 0; counter < slides[slide]["effects"].length; counter++)
			{
				for (var subCounter = 0; subCounter < slides[slide]["effects"][counter].length; subCounter++)
				{
					var effect = slides[slide]["effects"][counter][subCounter];
					if (effect["effect"] == "fade")
						fade(effect["dir"], effect["element"], STATE_END, effect["options"]);	
					else if (effect["effect"] == "appear")
						appear(effect["dir"], effect["element"], STATE_END, effect["options"]);	
					else if (effect["effect"] == "pop")
						pop(effect["dir"], effect["element"], STATE_END, effect["options"]);	
				}
			}
		}
		else if (state == STATE_START)
		{
			for (var counter = slides[slide]["effects"].length - 1; counter >= 0; counter--)
			{
				for (var subCounter = 0; subCounter < slides[slide]["effects"][counter].length; subCounter++)
				{
					var effect = slides[slide]["effects"][counter][subCounter];
					if (effect["effect"] == "fade")
						fade(parseInt(effect["dir"]) * -1, effect["element"], STATE_START, effect["options"]);	
					else if (effect["effect"] == "appear")
						appear(parseInt(effect["dir"]) * -1, effect["element"], STATE_START, effect["options"]);	
					else if (effect["effect"] == "pop")
						pop(parseInt(effect["dir"]) * -1, effect["element"], STATE_START, effect["options"]);	
				}
			}
		}
	}
}

/** Convenience function to translate a attribute string into a dictionary.
 *
 *	@param str the attribute string
 *  @return a dictionary
 *  @see dictToPropStr
 */
function propStrToDict(str)
{
	var list = str.split(";");
	var obj = new Object();

	for (var counter = 0; counter < list.length; counter++)
	{
		var subStr = list[counter];
		var subList = subStr.split(":");
		if (subList.length == 2)
		{
			obj[subList[0]] = subList[1];
		}	
	}

	return obj;
}

/** Convenience function to translate a dictionary into a string that can be used as an attribute.
 *
 *  @param dict the dictionary to convert
 *  @return a string that can be used as an attribute
 *  @see propStrToDict
 */
function dictToPropStr(dict)
{
	var str = "";

	for (var key in dict)
	{
		str += key + ":" + dict[key] + ";";
	}

	return str;
}

/** Sub-function to add a suffix to the ids of the node and all its children.
 *	
 *	@param node the node to change
 *	@param suffix the suffix to add
 *	@param replace dictionary of replaced ids
 *  @see suffixNodeIds
 */
function suffixNoneIds_sub(node, suffix, replace)
{
	if (node.nodeType == 1)
	{
		if (node.getAttribute("id"))
		{
			var id = node.getAttribute("id")
			replace["#" + id] = id + suffix;
			node.setAttribute("id", id + suffix);
		}

		if ((node.nodeName == "use") && (node.getAttributeNS(NSS["xlink"], "href")) && (replace[node.getAttribute(NSS["xlink"], "href")]))
			node.setAttribute(NSS["xlink"], "href", node.getAttribute(NSS["xlink"], "href") + suffix);

		if (node.childNodes)
		{
			for (var counter = 0; counter < node.childNodes.length; counter++)
				suffixNoneIds_sub(node.childNodes[counter], suffix, replace);
		}
	}
}

/** Function to add a suffix to the ids of the node and all its children.
 *	
 *	@param node the node to change
 *	@param suffix the suffix to add
 *  @return the changed node
 *  @see suffixNodeIds_sub
 */
function suffixNodeIds(node, suffix)
{
	var replace = new Object();

	suffixNoneIds_sub(node, suffix, replace);

	return node;
}

