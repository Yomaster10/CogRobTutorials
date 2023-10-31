(define (problem matchcellar-problem)
 (:domain matchcellar-domain)
 (:objects
   f1 f2 f3 - fuse
   m1 m2 m3 - match
 )
 (:init (handfree))
 (:goal (and (fuse_mended f1) (fuse_mended f2) (fuse_mended f3)))
)
