@echo off
grep -l "@%1@" TC* 2>NUL | sed -e "s:.txt::gI" -e "s:.py::gI" -e "s:.xml::gI" | sort | uniq | xargs