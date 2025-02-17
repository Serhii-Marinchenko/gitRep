#lang racket

;#1
(define (sequence low high stridle)
  (cond [(> low high) null]
        [#t (cons low (sequence (+ low stridle) high stridle))]))

;#2
(define (string-append-map xs suff)
      (map (lambda (i)
             (string-append suff i))
           xs))

;#3
(define (list-nth-mod xs n)
  (cond [(< n 0) (error "list-nth-mod: negative number")]
        [(null? xs) (error "list-nth-mod: empty list")]
        [#t (letrec ([i (remainder n (length xs))]
                     [f (lambda (xs i)
                          (if (= i 0)
                              (car xs)
                              (f (cdr xs) (- i 1))))])
              (f xs i))]))

;#4
(define (stream-for-n-steps s n)
  (if (= n 1)
      (cons (car (s)) null)
      (cons (car (s)) (stream-for-n-steps (cdr (s)) (- n 1)))))

;#5
(define funny-number-stream
  (letrec ([f (lambda (i)
                (if (= (remainder i 5) 0)
                    (cons (- i) (lambda () (f (+ 1 i))))
                    (cons i (lambda () (f (+ 1 i))))))])
  (lambda () (f 1))))

;#6
(define dan-then-dog
  (letrec ([f1 (lambda () (cons "dan.jpg" f2))]
           [f2 (lambda () (cons "dog.jpg" f1))])
    f1))

;#7
(define (stream-add-zero s)
  (lambda () (cons (cons 0 (car (s))) (stream-add-zero (cdr (s))))))

;#8
(define (cycle-lists xs ys)
  (letrec ([f1 (lambda (l) (if (null? l)
                                (f1 xs)
                                (cons (car l) (lambda () (f1 (cdr l))))))]
           [f2 (lambda (l) (if (null? l)
                                (f2 ys)
                                (cons (car l) (lambda () (f2 (cdr l))))))]
           [f3 (lambda (s1 s2) (cons (cons (car (s1)) (car (s2))) (lambda () (f3 (cdr (s1)) (cdr (s2))))))])
    (f3 (lambda () (f1 xs)) (lambda () (f2 ys)))))

;#9
(define (vector-assoc v vec)
  (letrec([aux (lambda (i)
                 (if (equal? (vector-length vec) i)
                     #f
                     (let* ([el (vector-ref vec i)])
                       (if (and (pair? el) (= (car el) v))
                           el
                           (aux (+ i 1))))))])
    (aux 0)))
                                        
;#10
(define (cached-assoc xs n)
  (letrec ([cach (make-vector n #f)]
           [i 0]
           [aux (lambda (xs)
                    (lambda (v)
                      (let ([isin (vector-assoc v cach)])
                        (if isin
                            (cdr isin)
                            (let ([new (assoc v xs)])
                              (begin
                                (vector-set! cach i new)
                                (if (= i (- n 1))
                                    (set! i 0)
                                    (set! i (+ i 1)))
                                    new))))))])
    (aux xs)))
                                

















