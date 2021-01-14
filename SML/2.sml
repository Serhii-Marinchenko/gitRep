fun all_except_option (arg : string * string list) =
    let
	fun aux (arg : string * string list, acc) =
	    case arg of
		(s, []) => NONE
	      | (s, x::[]) => if s = x then SOME []
			      else NONE
	      | (s, x1::xs) => if s = x1 then SOME (acc@xs)
				   else (aux ((s, xs), acc@[x1]))
    in
	aux (arg, [])
    end;

fun get_substitutions1 (arg : string list list * string) =
    let
	fun get_item (x) =
	    case x of
		NONE => []
	      | SOME i => i 
    in
    case arg of
	([], s) => []
      | (x::[], s) => get_item (all_except_option (s, x))
      | (x::xs, s) => get_item (all_except_option (s, x)) @ get_substitutions1 (xs, s)
    end;

fun get_substitutions2 (arg : string list list * string) =
        let
	    fun get_item (x) =
		case x of
		    NONE => []
		  | SOME i => i
	    fun aux (arg, acc) =
	    case arg of
		([], s) => acc
	      | (x::xs, s) => aux ((xs, s), acc @ get_item (all_except_option (s, x)))
	in aux (arg, [])
	end;

fun similar_names (x : string list list, y : {first:string,middle:string,last:string}) =
    let
	fun aux ({middle = b, last = c}, acc, substitutions : string list) =
	    case substitutions of
		[] => acc
	      | sub::subs => aux ({middle = b, last = c}, acc @ [{first = sub, middle = b, last = c}], subs)
    in
	case y of
	    {first = a, middle = b, last = c} => aux ({middle = b, last = c}, [], (a::get_substitutions2 (x, a)))
    end;

(* PART 2 *)
datatype suit = Clubs | Diamonds | Hearts | Spades;
datatype rank = Jack | Queen | King | Ace | Num of int;
type card = suit * rank;
datatype color = Red | Black;
datatype move = Discard of card | Draw;
exception NoSuchCard;
exception IllegalMove;


fun card_color (arg : card) =
    case arg of
	(Clubs, _) => Black
      | (Spades, _) => Black
      | (Diamonds, _) => Red
      | (Hearts, _) => Red;

fun card_value (arg : card) =
    case arg of
	(_, Num i) => i
      | (_, Jack) => 10
      | (_, Queen) => 10
      | (_, King) => 10
      | (_, Ace) => 11;

fun remove_card (cs : card list, c : card, e : exn) =
    let
	fun aux (acc, cs) =
	    case (acc, cs) of
		(acc, card::cards) => if card = c then acc @ cards else aux (acc@[card], cards)
	      | (acc, []) => raise e
    in
	aux ([], cs)
    end;

fun all_same_color (arg : card list) =
    case arg of
	x1 :: x2 :: xs => card_color (x1) = card_color (x2) andalso all_same_color (x2 :: xs)
      | x1 :: [] => true
      | [] => true;

fun sum_cards (arg : card list) =
    let
	fun aux (acc, arg) =
	    case arg of
		x::xs => aux ((acc + card_value(x)), xs)
	      | [] => acc;
    in
	aux (0, arg)
    end;

fun score (arg : card list, goal : int) =
    let
	val sum = sum_cards (arg)
    in
	let
	    val prelim_score = if sum > goal then (sum - goal) * 3
			       else (goal - sum)
	in
	    if all_same_color (arg) then prelim_score div 2
	    else prelim_score
	end
    end;

fun officiate (cds : card list, m : move list, goal : int) =
    let
	fun aux (held_cards : card list, cds, m) =
	    case (held_cards, cds, m) of
		(_, _, (Discard card)::moves) => aux (remove_card (held_cards, card, IllegalMove), cds, moves)
	      | (_, _, []) => score (held_cards, goal)
	      | (_, [], _) => score (held_cards, goal)
	      | (h::hs, c::cs, Draw::moves) => if sum_cards (c::h::hs) > goal then score (c::h::hs, goal)
					       else aux (c::held_cards, cs, moves)
	      | ([], c::cs, Draw::moves) => aux (c::held_cards, cs, moves)
    in
	aux ([], cds, m)
    end;
