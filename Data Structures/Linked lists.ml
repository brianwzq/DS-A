(* 
A collection of functions over linked lists in OCaml. 
Author: Brian   
*)

(* ***************** *)

(* Higher-order functions *)

let fold_right_list nil_case cons_case vs_init =
  (* val fold_right_list : 'a -> ('b -> 'a -> 'a) -> 'b list -> 'a *)
  let rec visit vs =
    match vs with
    | [] ->
       nil_case
    | hd :: tl ->
       cons_case hd (visit tl)
  in visit vs_init;;

let fold_left_list nil_case cons_case vs_init =
 (* fold_left_list : 'a -> ('b -> 'a -> 'a) -> 'b list -> 'a *)
  let rec visit vs s =
    match vs with
    | [] ->
       s
    | v :: vs' ->
       visit vs' (cons_case v s)
  in visit vs_init nil_case;;

(* ***************** *)

(* Identity functions *)

let test_identity candidate =
  (* val test_identity : (int list -> int list) -> bool *)
  (candidate [] = [])
  && (candidate [1] = [1])
  && (candidate [1; 2; 3] = [1; 2; 3]);;

let rec identity_v1 vs =
  (* val identity_v1 : 'a list -> 'a list *)
  match vs with
  | [] ->
     []
  | v :: vs' ->
     v :: (identity_v1 vs');;

let identity_v2 vs =
  (* val identity_v2 : 'a list -> 'a list *)
  let rec visit vs s =
    match vs with
    | [] ->
       s
    | v :: vs' ->
       visit vs' (v :: s)
  in List.rev (visit vs []);;

let () = assert (test_identity identity_v1
                 && test_identity identity_v2;;
  
(* ***************** *)  
  
(* Reversing a list *)

let test_reverse candidate =
  (* val test_reverse : (int list -> int list) -> bool *)
  (candidate [] = [])
  && (candidate [1] = [1])
  && (candidate [1; 2; 3] = [3; 2; 1]);;

(* A version using append *)
  
let rec reverse_v1 vs =
  (* val reverse_v1 : 'a list -> 'a list *)
  match vs with
  | [] ->
     []
  | v :: vs' ->
     List.append (reverse_v1 vs') [v];;

(* A tail-recursive version using a stack *)

let reverse_v2 vs =
  (* val reverse_v2 : 'a list -> 'a list  *)
  let rec visit vs s =
    match vs with
    | [] ->
       s
    | v :: vs' ->
       visit vs' (v :: s)
  in visit vs [];;

(* Expressing reverse_v1 using fold_right *)

let reverse_v3 vs =
  (* val reverse_v3 : 'a list -> 'a list *)
  fold_right_list []
                  (fun a b ->
                    List.append b [a])
                  vs;;

(* Expressing reverse_v2 using fold_left *)

let reverse_v4 vs =
  (* val reverse_v4 : 'a list -> 'a list *)
  fold_left_list []
                 (fun a b -> a :: b)
                 vs;;

(* Expressing reverse_v2 using fold_right *)

let reverse_v5 vs =
  (* val reverse_v5 : 'a list -> 'a list *)
  fold_right_list (fun s -> s)
                  (fun a b s ->
                    b (a :: s))
                  vs
                  [];;
  
let running_reverse_tests = test_reverse reverse_v1
                            && test_reverse reverse_v2
                            && test_reverse reverse_v3
                            && test_reverse reverse_v4
                            && test_reverse reverse_v5;;

(* ***************** *) 
  
(* Splitting a list *) 

let test_split candidate =
  (* val test_split : (int list -> int -> int list list) -> bool *)
  let vs1 = [1; 2; 3; 4; 5; 6; 7; 8; 9] in
  ((candidate vs1 1) = [[1]; [2]; [3]; [4]; [5]; [6]; [7]; [8]; [9]])
  && ((candidate vs1 2) = [[1; 2]; [3; 4]; [5; 6]; [7; 8]; [9]])
  && ((candidate vs1 3) = [[1; 2; 3]; [4; 5; 6]; [7; 8; 9]])
  && ((candidate [] 3) = [[]]);;

let split vs n_init =
  let rec visit_sublist xs n s =
    match xs with
    | [] ->
       ([], List.rev s)
    | x :: xs' ->
       if n = 0
       then (xs, List.rev s)
       else visit_sublist xs' (n - 1) (x :: s)
  and visit_mainlist ys =
    let (zs, s) = visit_sublist ys n_init [] in
    match zs with 
    | [] ->
       [s]
    | _ ->
       s :: (visit_mainlist zs)
  in
  visit_mainlist vs;;
    
let () = assert(test_split split);;

(* ***************** *)

(* Testing for a palindrome *) 

let test_palindrome candidate =
  (* val test_palindrome : (int list -> bool) -> bool *)
  (candidate [] = true)
  && (candidate [1] = true)
  && (candidate [1; 2] = false)
  && (candidate [1; 2; 3] = false)
  && (candidate [1; 2; 3; 2; 1] = true)
  && (candidate [1; 2; 2; 1] = true);;

(* Version 1: Reversing then checking half *)

let palindrome_v1 vs =
  (* val palindrome_v1 : 'a list -> bool *)
  let rec reverse_and_count vs s n =
    (* val reverse_and_count : 'a list -> 'a list -> int -> 'a list * int *)
    match vs with
    | [] ->
       (s, n)
    | v :: vs' ->
       reverse_and_count vs' (v :: s) (n + 1)
  and visit vs s n =
    (* val visit : 'a list -> 'a list -> int -> bool *)
    match (vs, s) with
    | [], [] ->
       true
    | (v :: vs', x :: xs') ->
       if n = 0
       then true
       else (v = x) && visit vs' xs' (n - 1)
    | _ ->
       false
  in let (s, n) = reverse_and_count vs [] 0
     in visit vs s n;;

let () = assert(test_palindrome palindrome_v1);;

(* Passes the test. Complexity = O(3n/2). Takes n to reverse the list and count, and then n/2 to do the checking. *)

(* Version 2: TABA Continuation-pasing-style *)

let palindrome_v2 l =
  (* val palindrome_v2 : 'a list -> bool *)
  let rec visit l1 l2 k =
    match (l1, l2) with
    | (x1 :: xs1', x2 :: x2' :: xs2') ->
       visit xs1' xs2' (fun xs -> match xs with
                                  | [] ->
                                     false
                                  | x :: xs' -> if x = x1
                                                then k xs'
                                                else false)
    | (x1 :: xs1', x2 :: []) -> (* Odd case *)
       k xs1'
    | (x1 :: xs1', []) -> (* Even case *)
       k l1
    | (_ , _) ->
       true
  in
  visit l l (fun a -> true);;

let () = assert(test_palindrome palindrome_v2);;  

(* Lazy lists *)

type 'a lazy_list =
  | Lnil
  | Lcons of 'a * 'a lazy_list Lazy.t;;

let lazy_option_map f x =
  match x with
  | lazy (Some x) ->
     Some (Lazy.force f x)
  | _ ->
     None;;

let x = Lcons (3, lazy Lnil);;      

