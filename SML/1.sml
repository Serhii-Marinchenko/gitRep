fun is_older (x : int * int* int, y : int * int * int) =
    #1 x < #1 y
    orelse (#1 x = #1 y andalso #2 x < #2 y)
    orelse (#1 x = #1 y andalso #2x = #2 y andalso #3 x < #3 y);
  
fun number_in_month (x : (int * int * int) list, y : int) =
    if null x
    then 0
    else if #2 (hd x) <> y
    then number_in_month (tl x, y)
    else 1 + number_in_month (tl x, y);

fun number_in_months (x : (int * int * int) list, y : int list) =
    if null x orelse null y
    then 0
    else number_in_month (x, hd y) + number_in_months (x, tl y);

fun dates_in_month (x : (int * int * int) list, y : int) =
    if null x then []
    else if #2 (hd x) = y then hd x :: dates_in_month (tl x, y)
    else dates_in_month (tl x, y);

fun dates_in_months (x : (int * int * int) list, y : int list) =
    if null x orelse null y then []
    else dates_in_month (x, hd y) @ dates_in_months (x, tl y);

fun get_nth (x : string list, y : int) =
    if y = 1 then hd x
    else get_nth(tl x, y-1);

fun date_to_string (x : int * int * int) =
    let val m = ["January ", "February ", "March ", "April ", "May ", "June ", "July ", "August ", "September ", "October ", "November ", "December "]
    in  get_nth (m, #2 x) ^ Int.toString (#3 x) ^ ", " ^ Int.toString ( #1 x)
    end;

fun number_before_reaching_sum (sum : int, lst : int list) =
    if sum <= hd lst
    then 0
    else 1 + number_before_reaching_sum(sum - hd lst, tl lst);

fun what_month (x : int) =
    let
	val days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    in number_before_reaching_sum (x, days) + 1
    end;

fun month_range (day1 : int, day2 : int) =
    let fun count (from : int, to : int) =
	    if from > to then []
	    else what_month(from) :: count (from + 1, to)
    in count (day1, day2)
    end;

fun oldest (x : (int * int * int) list) =
    if null x then NONE
    else let
	fun older (x : int * int* int, y : int * int * int) =
	    if #1 x < #1 y
	    then x
	    else
		let val month = #1 x = #1 y andalso #2 x < #2 y
		in if month
		   then x
		   else let
		       val day = #1 x = #1 y andalso #2x = #2 y andalso #3 x < #3 y
		   in if day
		      then x
		      else y
		   end
		end
    in let
	fun is_oldest (l : (int * int * int) list) =
	    if null (tl l) then hd l
	    else older (hd l, is_oldest (tl l))
    in SOME (is_oldest(x))
    end
    end;
