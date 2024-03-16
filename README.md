mrsync(1)                                                              mrsync(1)



NAME
       mrsync - minimalistic version of rsync

SYNOPSIS
       mrsync [OPTION]... SRC [SRC]... DEST


       mrsync [OPTION]... SRC

DESCRIPTION
       mrsync is a program that behaves in much the same way that rsync does, but
       has less options. 

GENERAL
       mrsync copies files either to or from a remote host, or locally  on  the
       current  host  (it  does  not  support copying files between two remote
       hosts).

       This version only works for local file synchronizations.



USAGE
       You use mrsync in the same way you use rcp. You must  specify  a  source
       and a destination, one of which may be remote.

       Perhaps the best way to explain the syntax is with some examples:

              mrsync -av foo:src/bar /data/tmp


       This would recursively transfer all files from the directory src/bar on
       the machine foo into the /data/tmp/bar directory on the local  machine.
       The  files  are  transferred in "archive" mode, which ensures that
       permissions are preserved  in  the transfer.  

              mrsync -av foo:src/bar/ /data/tmp


       A trailing slash on the source changes this behavior to avoid  creating
       an  additional  directory level at the destination.  You can think of a
       trailing / on a source as meaning "copy the contents of this directory"
       as  opposed  to  "copy  the  directory  by name", but in both cases the
       attributes of the containing directory are transferred to the  contain-
       ing  directory on the destination.  In other words, each of the follow-
       ing commands copies the files in the same way, including their  setting
       of the attributes of /dest/foo:

              mrsync -av /src/foo /dest
              mrsync -av /src/foo/ /dest/foo


       You can use mrsync in local-only mode, where both the source and
       destination don't have a ':' in the name. In this case it behaves  like
       an improved copy command.



OPTIONS SUMMARY
       Here is a short summary of the options available in mrsync. Please refer
       to the detailed description below for a complete description.

        -r, --recursive             recurse into directories
        --timeout=TIME          set I/O timeout in seconds
	--list-only             list the files instead of copying them


       mrsync  can also be run as a daemon, in which case the following options
       are accepted:

            --daemon                run as an mrsync daemon
            --address=ADDRESS       bind to the specified address
            --no-detach             do not detach from the parent
            --port=PORT             listen on alternate port number
        -h, --help                  show this help (if used after --daemon)



OPTIONS
       Many  of  the  command  line options  have  two  variants,  one short and 
       one long.  These are shown below, separated by commas. Some options only 
       have a long variant.  The '='  for  options  that take a parameter is 
       optional; whitespace can be used instead.


       -r, --recursive
              This  tells  mrsync  to  copy  directories recursively.  See also
              --dirs (-d).


       --timeout=TIMEOUT
              This option allows you to set a maximum I/O timeout in  seconds.
              If no data is transferred for the specified time then mrsync will
              exit. The default is 0, which means no timeout.


       --list-only
              This  option will cause the source files to be listed instead of
              transferred.  This option is  inferred  if  there  is  a  single
              source  arg  and no destination specified, so its main uses are:
              (1) to turn a copy command that includes a destination arg  into
              a  file-listing command, (2) to be able to specify more than one
              local source arg (note: be sure to include the destination).
              Caution: keep in mind that a source arg with a wild-card is 
              expanded by the shell into multiple args, so it is never safe to 
              try to list such an arg without using this option.  For example:

                  mrsync -av --list-only foo* dest/


SYMBOLIC LINKS
       Symbolic links are  not  transferred  at  all.   A  message
       "skipping non-regular" file is emitted for any symlinks that exist.

DIAGNOSTICS
       mrsync occasionally produces error messages that may seem a little cryp-
       tic. The one that seems to cause the most confusion is  "protocol  ver-
       sion mismatch -- is your shell clean?".

       This  message is usually caused by your startup scripts or remote shell
       facility producing unwanted garbage on the stream that mrsync  is  using
       for  its  transport.  The  way  to diagnose this problem is to run your
       remote shell like this:

              ssh remotehost /bin/true > out.dat


       then look at out.dat. If everything is working correctly  then  out.dat
       should  be  a zero length file. If you are getting the above error from
       mrsync then you will probably find that out.dat contains  some  text  or
       data.  Look  at  the contents and try to work out what is producing it.
       The most common cause is incorrectly configured shell  startup  scripts
       (such  as  .cshrc  or .profile) that contain output statements for non-
       interactive logins.




SEE ALSO
       rsync(1)


BUGS
       * Do not work when using '.' as destination (just change directory then use new relative-path as destination).
       * Looping at end of program (use ctrl+C)
       * We did not try the program with symbolic links.


INTERNAL OPTIONS
       The option --server is used  internally  by  mrsync,  and
       should  never  be  typed  by  a  user under normal circumstances.


CREDITS
       A  WEB site is available at http://rsync.samba.org/.  The site includes
       an FAQ-O-Matic which may cover  questions  unanswered  by  this  manual
       page.

AUTHORS
       This mrsync has been written by YOUNES Mohamed and BENHARRATS Nadir.

                                  L2 info math-info 2023              mrsync(1)
