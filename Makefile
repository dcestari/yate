osx: osx_app fix_i386

osx_app:
	python2.6 setup_osx.py py2app

fix_i386:
	ditto --arch i386 dist/yate.app/Contents/MacOS/yate{,_i386}
	mv dist/yate.app/Contents/MacOS/yate{_i386,}

