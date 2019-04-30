SRC_DIR=./

# go
DST_DIR=./auto_generated_go
mkdir -p $DST_DIR
protoc -I=$SRC_DIR --go_out=$DST_DIR $SRC_DIR/news.proto

# python
DST_DIR=./auto_generated_python
PYTHON_PROJECT=../../py/saga/saga/
mkdir -p $DST_DIR
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/news.proto
rm -rf $PYTHON_PROJECT$DST_DIR/*
cp -r $DST_DIR $PYTHON_PROJECT
