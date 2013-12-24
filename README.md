phd-thesis-tjhunter
===================

All the files to build my phd thesis.


Requirements
============

To build from scratch, you need the following programs. The versions
indicated have been tested, other versions may work as well.

- python >= 2.5
- lyx
- unoconv (openoffice)
- wget/curl
- convert (imagemagick)

You need the following python packages:
- numpy
- scipy
- matplotlib

Compilation instructions
========================

```bash
wget http://waf.googlecode.com/files/waf-1.7.11
mv waf-1.7.11 waf
chmod 755 waf
./waf -j1 -vvv distclean configure build --data-dir=/home/tjhunter/work/data/thesis
./waf -j1 build

```

Edit a lyx file. Make sure to include the location of the images:
TEXINPUTS=$PWD::$PWD/build lyx


Berkeley requirements
======================

http://www.grad.berkeley.edu/policies/pdf/disguide.pdf
http://grad.berkeley.edu/policies/guides/dissertation
https://buffy.eecs.berkeley.edu/PHP/facres/menu.php?f_submit=gradrpts&studid=

 The Dissertation

Filing your doctoral dissertation at the Graduate Division is one of the final steps leading to the award of your graduate degree. It is imperative that you carefully follow Graduate Division's Instructions for Preparing and Filing Your Thesis or Dissertation. Graduate Division strictly enforces rules about margin widths, page numbering, etc., and the Graduate Degrees Office in 318 Sproul Hall is the official source of all answers regarding any aspect of preparing your manuscript. You are REQUIRED to read the Dissertation Filing Guidelines (for Doctoral Students). In addition to electronically submitting your dissertation to Graduate Division, a copy should also be uploaded to the EECS Department Website through the online submission form. The Department no longer accepts a hard copy of your dissertation. The documents you must submit to the EECS Grad Office are:

    a copy of the signed signature page
    a copy/printout of the title page
    a copy/printout of the abstract

If you want a Certificate of Completion of the Ph.D., be sure to mention this to the Graduate Division when you file your dissertation. The Request for Certificate of Completion is available online.

Your diploma will not be ready for a number of months. You may arrange to have it mailed to you when it is ready by completing the Diploma Request Form found on the Registrar's website 
