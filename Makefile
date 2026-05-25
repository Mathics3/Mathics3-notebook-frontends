# A GNU Makefile to run various tasks - compatibility for us old-timers.

# Note: This makefile include remake-style target comments.
# These comments before the targets start with #:
# remake --tasks to shows the targets and the comments

.PHONY: all \
   ChangeLog-without-corrections \
   dist \
   run-jupyter-notebook \
   run-jupyter-console \
   rmChangeLog

GIT2CL ?= admin-tools/git2cl

#: Make distribution: wheels and tarball
dist:
	./admin-tools/make-dist.sh

#: Run a Jupyter notebook
run-jupyter-notebook:
	jupyter notebook

#: Run a Jupyter console
run-jupyter-console:
	jupyter console

#: Remove ChangeLog
rmChangeLog:
	$(RM) ChangeLog || true

#: Create ChangeLog from version control without corrections
ChangeLog-without-corrections:
	git log --pretty --numstat --summary | $(GIT2CL) >ChangeLog

#: Create a ChangeLog from git via git log and git2cl
ChangeLog: rmChangeLog ChangeLog-without-corrections
	patch ChangeLog < ChangeLog-spell-corrected.diff
