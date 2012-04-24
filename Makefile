osx: osx_app fix_i386

osx_app:
	python2.6 setup_osx.py py2app

fix_i386:
	ditto --arch i386 dist/Yate.app/Contents/MacOS/Yate{,_i386}
	mv dist/Yate.app/Contents/MacOS/Yate{_i386,}

clean:
	rm -Rf dist build

