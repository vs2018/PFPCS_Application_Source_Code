import os, sys

# Source: Author: beoliver, Date:Feb 2 '12 at 22:42, URL: https://stackoverflow.com/questions/4934806/how-can-i-find-scripts-directory-with-python/9121110#9121110
# Source: Author: jbcurtin, Date:Feb 9 '11 at 7:01, URL: https://stackoverflow.com/questions/4934806/how-can-i-find-scripts-directory-with-python/9121110#9121110
# Source: https://nayarweb.com/blog/category/technology/page/2/

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
