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
- inkscape (from the command line)

You need the following python packages:
- numpy
- scipy
- matplotlib

Compilation instructions
========================

```bash
./get_waf.sh
./waf -j1 -vvv distclean configure build
./waf -j1 build

```

Edit a lyx file. Make sure to include the location of the images:
TEXINPUTS=$PWD::$PWD/build lyx


Berkeley requirements
======================

To push to the website:
```bash
scp -i ~/.ssh/id_rsa build/thesis.pdf tjhunter@login.eecs.berkeley.edu:/home/eecs/tjhunter/public_html/publications/thesis.pdf
```

The file is available at:

http://www.eecs.berkeley.edu/~tjhunter/publications/thesis.pdf

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
