clc
close all
clear all
Dc= rand(1000, 2);
W= [1,-1,1];

Ds_new= [ones(1000, 1), Dc];
resultado= logical(Ds_new * W' > 0);
conteo_ceros = sum(~resultado);
