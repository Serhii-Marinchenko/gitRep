exception NoAnswer;

datatype pattern = Wildcard
		 | Variable of string
		 | UnitP
		 | ConstP of int
		 | TupleP of pattern list
		 | ConstructorP of string * pattern;
						

datatype valu = Const of int
	      | Unit
	      | Tuple of valu list
	      | Constructor of string * valu;
					    
fun g f1 f2 p =
    let 
	val r = g f1 f2 
    in
	case p of
	    Wildcard          => f1 ()
	  | Variable x        => f2 x
	  | TupleP ps         => List.foldl (fn (p,i) => (r p) + i) 0 ps
	  | ConstructorP(_,p) => r p
	  | _                 => 0
    end;

fun head arg = (* avoid using hd *)
    case arg of
	x::xs => x
      | _ => raise Empty;

fun tail arg = (* avoid using tl *)
    case arg of
	x::xs => xs
      | _ => raise Empty;

fun is_empty arg = (* avoid using null *)
    case arg of
	[] => true
      | _ => false;
    
(* Task 1 *)
fun curry f y x = f (x, y);
fun only_capitals (arg : string list) = List.filter (fn x => Char.isUpper (curry String.sub 0 x)) arg;

(*Task 2 *)
fun longest_string1 (arg : string list) =
    foldl (fn (x, y) => if String.size x > String.size y then x else y) "" arg;

(* #3 *)
fun longest_string2 (arg : string list) =
    foldl (fn (x, y) => if String.size (x) >= String.size (y) then x else y) "" arg;

fun longest_string_helper f =
    fn s => foldl (fn (s1, s2) => if f (String.size s1, String.size s2)
				   then s1
				   else s2)
		   ""
		   s;

val longest_string3 = longest_string_helper (fn (x, y) =>  x > y);
val longest_string4 = longest_string_helper (fn (x, y) => x >= y);

(* 5 *)
fun longest_capitalized sl = (longest_string1 o only_capitals) sl;

(* 6 *)
fun rev_string (arg : string) =
    (String.implode o List.rev o String.explode) arg;

(* 7 *)
fun first_answer f lst =
    case (lst, (f (head lst)) handle Empty => raise NoAnswer) of
	([], _) => raise NoAnswer
      | (x::xs, NONE) => first_answer f xs
      | (x::xs, SOME v) => v;

(* 8 *)
fun all_answers f lst =
    let
	fun aux (acc, n, lst) =
	    if n > 0 then NONE
	    else
		if is_empty lst then SOME acc
		else
		    case f (head lst) of
			NONE => aux (acc, n + 1, tail lst)
		      | SOME v => aux (acc @ v, n, tail lst)
    in
	aux ([], 0, lst)
    end;

(* 9 *)
val count_wildcards = g (fn x => 1) (fn x => 0);

val count_wild_and_variable_lengths = g (fn x => 1) String.size;

fun count_some_var (s, p) = g (fn x => 0) (fn x => if s = x then 1 else 0) p;

(* 10 *)
fun check_pat p =
    let
	fun aux (p, acc : string list) =
	    case p of
		Variable x => aux (Wildcard, acc @ [x])
	      | TupleP ps => List.foldl aux acc ps
	      | ConstructorP(_, p) => aux (p, acc)
	      | _ => acc
    in
	let
	    val l = aux (p, [])
	in
	    let
		fun aux2 (acc, lst) =
		    if acc then false
		    else
			case lst of
			    x::xs => aux2 (List.exists (fn j => j = x) xs, xs)
			  | [] => not acc
	    in aux2 (false, l)
	    end
	end
    end;

(* 11 *)
fun match arg =
    case arg of
	(v, Variable j) => SOME [(j, v)]
      | (_, Wildcard)         => SOME []
      | (Unit, UnitP)         => SOME []
      | (Const i, ConstP j)   => if i = j
				 then SOME []
				 else NONE
      | (Constructor(s1, v : valu), ConstructorP(s2, p : pattern)) => if s1 = s2
								      then match (v, p)
								      else NONE
      | (Tuple vs, TupleP ps) => if length vs = length ps
				 then all_answers match (ListPair.zip (vs, ps))
				 else NONE
      | _ => NONE;

(* 12 *)
fun curry1 f x y = f (x, y)
fun first_match v pl = SOME ((first_answer (curry1 match v) pl)) handle NoAnswer => NONE;
