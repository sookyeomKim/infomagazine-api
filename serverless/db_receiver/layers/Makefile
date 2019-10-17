clean:
	rm -rf build build.zip
	rm -rf __pycache__

build-layers-package: clean
	mkdir build
	cp -r lib build/.
	pip install --upgrade pip
	pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr db_receiver.zip .
	cp build/db_receiver.zip .
	rm -rf build