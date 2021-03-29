#lang racket
(require math/distributions)
(require math/statistics)
; Створимо 2 масиви історичних дохідностей за останні 20 років. Позначемо крпоративні американські облігації рейтингу Baa видом "А", високоризикові облігації – видом "Б" (ra та rb відповідно).
(define ra (list 0.0486 0.143 0.1101 0.0702 0.0147 0.037 0.0029 -0.0858 0.2377 0.066 0.0914 0.0789 -0.0248 0.0862 -0.0082 0.0899 0.0744 -0.0508 0.1275 0.091))
(define rb (list -0.0581 0.0544 -0.0153 0.2794 0.1195 0.0226 0.1192 0.0265 -0.2617 0.5422 0.1422 0.0547 0.1472 0.073 0.0077 -0.067 0.1443 0.0648 -0.0327 0.1488))
; Крок 1 та 2
(define (resemple arr)
  (letrec ([memo null]
           [get-rd-el (lambda (i)
                        (lambda (j)
                          (if (= i 0)
                              (car j)
                              ((get-rd-el (- i 1)) (cdr j)))))]
           [get-20-random-els (lambda (i)
                                (let ([random-el ((get-rd-el
                                                   (round (* (random) 19))) arr)])
                                  (if (= i 0)
                                      memo
                                      (begin
                                        (set! memo (cons random-el memo))
                                        (get-20-random-els (- i 1))))))])
    (get-20-random-els 20)))

(define (Monte-Carlo i arr resemple-fun)
  (letrec ([pseudo-sample (lambda () (resemple-fun arr))]
           [memo null]
           [iter (lambda (i) (if (= i 0)
                                 memo
                                 (begin
                                   (set! memo (cons (mean (pseudo-sample)) memo))
                                   (iter (- i 1)))))])
    (iter i)))
;3-й крок
(define µa (mean (Monte-Carlo 10000 ra resemple))) ;математичне сподівання облігацій виду А
(define µb (mean (Monte-Carlo 10000 rb resemple))) ;математичне сподівання облігацій виду Б
(define σa (stddev (Monte-Carlo 10000 ra resemple)));стандартне відхилення облігацій виду А
(define σb (stddev (Monte-Carlo 10000 rb resemple)));стандартне відхилення облігацій виду Б
; Крок 4, 5 та 6
(define (simulation-with-accuracy i la lb)
  (letrec ([z-randoms (lambda () (sample (normal-dist 0 1) i))]
           [transform-z-to-r (lambda (µ σ)
                               (lambda (z)
                                 (+ µ (* z σ))))]
           [z-ra (transform-z-to-r µa σa)]
           [z-rb (transform-z-to-r µb σb)]
           [map (lambda (arr f) (cond [(null? arr) null]
                                      [#t (cons (f (car arr))
                                                (map (cdr arr) f))]))]
           [est-ra (map (z-randoms) z-ra)]
           [est-rb (map (z-randoms) z-rb)]
           [zip (lambda (arr1 arr2)
                  (if (null? (or arr1 arr2))
                      null
                      (cons (cons (car arr1) (car arr2)) (zip (cdr arr1) (cdr arr2)))))]
           [est-ra-rb (zip est-ra est-rb)]
           [stateA? (lambda (arr) (map arr (lambda (pair) (> (car pair) (cdr pair)))))]
           [memo null]
           [accuracy (lambda (arr-bool arr-ra arr-rb la lb)
                       (cond [(null? (or arr-bool arr-ra arr-rb)) memo]
                             [(car arr-bool)
                              (if (< (random) la)
                                  (begin
                                    (set! memo (cons (car arr-ra) memo))
                                    (accuracy (cdr arr-bool) (cdr arr-ra) (cdr arr-rb) la lb))
                                  (begin
                                    (set! memo (cons (car arr-rb) memo))
                                    (accuracy (cdr arr-bool) (cdr arr-ra) (cdr arr-rb) la lb)))]
                             [#t (if (< (random) lb)
                                     (begin
                                       (set! memo(cons (car arr-rb) memo))
                                       (accuracy
                                        (cdr arr-bool) (cdr arr-ra) (cdr arr-rb) la lb))
                                     (begin
                                       (set! memo (cons (car arr-ra) memo))
                                       (accuracy (cdr arr-bool) (cdr arr-ra) (cdr arr-rb) la lb)))]))]
           [returns (accuracy (stateA? est-ra-rb) est-ra est-rb la lb)])
    (mean returns)))

;uncomment to run the programm
;(simulation-with-accuracy 10000 0.9 0.8)
           












