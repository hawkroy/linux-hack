#!/bin/sh 
/home/zhengwa1/opt/qemu-1.7.1/bin/qemu-system-i386 -fda $1 -fdb rootimage-0.11-my -s -S -monitor stdio -debugcon file:debug.log -global isa-debugcon.iobase=0x402
