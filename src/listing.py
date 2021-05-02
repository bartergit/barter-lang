listing = """
        func pass_ref (int x) void {
            cout(x)
            cout(deref(x))
            set_ref(x,10)
            set_ref(sum(x,1),15)
            set_ref(sum(x,2),20)
            return
        }
        func dec_ref (int ptr) void {
            set_ref(ptr,98)
            int z = 18
            int arr = dec_arr(a,3)
            cout(arr)
            cout(deref(arr))
            pass_ref(arr)
            cout(deref(sum(arr,0)))
            cout(deref(sum(arr,1)))
            cout(deref(sum(arr,2)))
            return
        }
        func main () void {
            //int x = 99
            int y = 3
            int ptr = ref(y)
            cout(ptr)
            dec_ref(ptr)
            cout(y)
            return
        }
        """
listing13 = """
            func pass_ref (int a) void {
                cout(a)
                set_ref(a,10)
                set_ref(sum(a,1),15)
                set_ref(sum(a,2),20)
                return
            }
            func dec_ref () void {
                int z = 18
                int arr = dec_arr(a,3)
                pass_ref(arr)
                cout(deref(sum(arr,0)))
                cout(deref(sum(arr,1)))
                cout(deref(sum(arr,2)))
                return
            }
            func main () void {
                int x = 19
                int broke = 20
                dec_ref()
                return
            }
            """
listing19 = """
            func pass_ref (int x) void {
                cout(x)
                cout(deref(x))
                set_ref(x,10)
                set_ref(sum(x,1),15)
                set_ref(sum(x,2),20)
                return
            }
            func dec_ref (int ptr) void {
                set_ref(ptr,98)
                int z = 18
                int arr = dec_arr(a,3)
                cout(arr)
                cout(deref(arr))
                pass_ref(arr)
                cout(deref(sum(arr,0)))
                cout(deref(sum(arr,1)))
                cout(deref(sum(arr,2)))
                return
            }
            func main () void {
                //int x = 99
                int y = 3
                int ptr = ref(y)
                cout(ptr)
                dec_ref(ptr)
                cout(y)
                return
            }
            """
listing5 = """
            func pass_ref (int x) void {
                int z = 18
                set_ref(x,10)
                set_ref(sum(x,1),15)
                set_ref(sum(x,2),20)
                return
            }
            func main () void {
                int y = 19
                int arr = dec_arr(a,3)
                cout(arr)
                cout(deref(arr))
                pass_ref(arr)
                cout(deref(sum(arr,0)))
                cout(deref(sum(arr,1)))
                cout(deref(sum(arr,2)))
                return
            }
            """
listing0 = """
            func change (int ptr) void {
                int n = 19
                cout(ptr)
                cout(deref(ptr))
                set_ref(ptr,99)
                return
            }
            func main () void {
                int x = 15
                int y = 3
                int ptr = ref(y)
                cout(ptr)
                cout(deref(ptr))
                change(ptr)
                cout(y)
                cout(ptr)
                cout(deref(ptr))
                return
            }
            """
listing88 = """
            func inc (int x) int {
                return sum(x,1)
            }
            func plus (int x int y) int {
                return sum(x,y)
            }
            func main () void {
                int x = 5
                int y = 19
                cout(plus(x,y))
                cout(inc(y))
                int res = plus(inc(inc(x)),y)
                cout(x)
                cout(y)
                if true {
                    cout(res)
                }
                return 
            }
            """
