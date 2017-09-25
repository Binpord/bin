startup_path=$(pwd)

cd ~
mkdir ycm_build
cd ycm_build
cmake -G "Unix Makefiles" -DUSE_SYSTEM_LIBCLANG=ON . ~/.vim/bundle/youcompleteme/third_party/ycmd/cpp
cmake --build . --target ycm_core
cd ..
rm -rf ycm_build
cd $startup_path
