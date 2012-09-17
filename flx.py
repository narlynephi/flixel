#!/usr/bin/env python

import os, sys
import argparse

parser = argparse.ArgumentParser(description="Script to setup basic Flixel project files")

# the only required argument of this script
parser.add_argument("project", metavar="PROJECT", type=str, default=None,
	help="Name of the new project")

# optional arguments
parser.add_argument("--width", metavar="N", type=int, default=320,
	help="Width of your game in 'true' pixels (ignoring zoom)")
parser.add_argument("--height", metavar="N", type=int, default=240,
	help="Height of your game in 'true' pixels (ignoring zoom)")
parser.add_argument("--zoom", metavar="N", type=int, default=2,
	help="How chunky you want your pixels")
parser.add_argument("--src", metavar="SRC", type=str, default="src",
	help="Name of the source folder under the project folder (if there is one!)")
parser.add_argument("--preloader", metavar="PRELOADER", type=str, default="Preloader",
	help="Name of the preloader class")
parser.add_argument("--menustate", metavar="MENUSTATE", type=str, default="MenuState",
	help="Name of the menu state class")
parser.add_argument("--playstate", metavar="PLAYSTATE", type=str, default="PlayState",
	help="Name of the play state class")
parser.add_argument("--noflex", action="store_true", default=False,
	help="Don't create a Default.css (for use with Flex Builder)")
parser.add_argument("--noact", action="store_true", default=False,
	help="Show where files will be created and what options will be used")

args = parser.parse_args()

#BASIC SCRIPT PRESETS
width = args.width				# Width of your game in 'true' pixels (ignoring zoom)
height = args.height			# Height of your game in 'true' pixels
zoom = args.zoom				# How chunky you want your pixels
src = args.src					# Name of the source folder under the project folder (if there is one!)
preloader = args.preloader		# Name of the preloader class
menuState = args.menustate		# Name of menu state class
playState = args.playstate		# Name of play state class
flexBuilder = not args.noflex	# Whether or not to generate a Default.css file
project = args.project			# name of the new project

preloaderPath = os.path.join(src, preloader+".as")
playStatePath = os.path.join(src, playState+".as")
projectPath = os.path.join(src, project+".as")
menuStatePath = os.path.join(src, menuState+".as")
defaultCssPath = os.path.join(src, "Default.css")

if args.noact:
	settings = """
Will run with the following options:
	width      : %d
	height     : %d
	zoom       : %d
	noflex     : %s
	src        : '%s'
	preloader  : '%s'
	play state : '%s'
	menu state : '%s'
	project    : '%s'
	""" % (
		width, height, zoom, "NO" if flexBuilder else "YES", src, preloader, playState, menuState, project,
	)
	print settings

	paths = [preloaderPath, playStatePath, projectPath, menuStatePath]
	if flexBuilder:
		paths.append(defaultCssPath)

	print("""
The following files will be written to:
%s
	""" % "\n".join(["\t"+path for path in paths]))

	exit(0)



def generate_file(path, code):
	try:
		fo = open(path, 'w')
	except IOError:
		print("Can't open '%s' for writing" % path)
		sys.exit()
	
	fo.write(code)
	fo.close()

	print("Wrote to '%s'" % path)


# ---------------------------
# Generate project code
# ---------------------------
project_code = """
package
{
	import org.flixel.*;
	[SWF(width="%d", height="%d", backgroundColor="#000000")]
	[Frame(factoryClass="Preloader")]
	public class %s extends FlxGame
	{
		public function %s()
		{
			super(%d, %d, %s, %d);
		}
	}
}
""" % (width, height, project, project, width, height, menuState, zoom)
generate_file(projectPath, project_code)


# ---------------------------
# Generate preloader code
# ---------------------------
preloader_code = """
package
{
	import org.flixel.system.FlxPreloader;
	public class %s extends FlxPreloader
	{
		public function %s()
		{
			className = "%s";
			super();
		}
	}
}
""" % (preloader, preloader, project)
generate_file(preloaderPath, preloader_code)


# ---------------------------
# Generate Default.css
# ---------------------------
if flexBuilder:
	default_css_code = 'Add this: "-defaults-css-url Default.css"\nto the project\'s additonal compiler arguments.'
	generate_file(defaultCssPath, default_css_code)


# ---------------------------
# Generate menu state code
# ---------------------------
menu_state_code = """
package
{
	import org.flixel.*;

	public class %s extends FlxState
	{
		override public function create(): void
		{
			var text:FlxText;
			text = new FlxText(0, FlxG.height/2-10, FlxG.width, "%s");
			text.size = 16;
			text.alignment = "center";
			add(text);
			text = new FlxText(FlxG.width/2-50, FlxG.height-20, 100, "click to play");
			text.alignment = "center";
			add(text);

			FlxG.mouse.show();
		}

		public override function update():void
		{
			super.update();

			if(FlxG.mouse.justPressed())
			{
				FlxG.mouse.hide();
				FlxG.switchState(new PlayState());
			}
		}
	}
}
""" % (menuState, project)
generate_file(menuStatePath, menu_state_code)


# ---------------------------
# Generate play state code
# ---------------------------
play_state_code = """
package
{
	import org.flixel.*;

	public class %s extends FlxState
	{
		override public function create(): void
		{
			add(new FlxText(0, 0, 100, "INSERT GAME HERE"));
		}
	}
}
""" % (playState)
generate_file(playStatePath, play_state_code)


print("\nDone!")