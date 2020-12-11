//Course Number:	CIS4362
//Course Name:		Cryptology
//Assignment Name:	Multi Cipher
//My Name:			Stephen Wehlburg
//Date:				December 10th 2020
import java.io.*;
import java.util.*;
import java.math.*;

public class ciphers
{
    static int get_val(char ch)
    {
        if ((65 <= ch) && (ch <= 73))
        {
            return ch - 65;
        }
        else if  ((74 <= ch) && (ch <= 90))
        {
            return ch - 66;
        }
        else
        {
            return -1;
        }
    }


    static char get_char(int num)
    {
        if ((0 <= num) && (num <= 7))
        {
            return (char)(65 + num);
        }
        else if ((8 <= num) && (num <= 25))
        {
            return (char)(66 + num);
        }
        else
        {
            return (char)(-1);
        }
    }

    static String rail_fence(String msg, int num_rails)
    {
        StringBuilder buffer = new StringBuilder();
        if(num_rails == 1)
        {
            for(int i = 0; i < msg.length(); ++i)
            {
                buffer.append(msg.charAt(i));
            }
        }
        else
        {
            ArrayList<ArrayList<Character>> rails = new ArrayList<>();
            ArrayList<Integer> real_lengths = new ArrayList<>();
            for(int i = 0; i < num_rails; ++i)
            {
                ArrayList<Character> temp = new ArrayList<>();
                rails.add(temp);
                real_lengths.add(0);
            }

            int cur_rail = 0;
            boolean down = true;
            for(int i = 0; i < msg.length(); ++i)
            {
                rails.get(cur_rail).add(msg.charAt(i));
                real_lengths.set(cur_rail, real_lengths.get(cur_rail) + 1);

                if(down) { ++cur_rail; }
                else { --cur_rail; }

                if(cur_rail == 0) { down = true; }
                else if(cur_rail == (num_rails - 1)) { down = false; }
            }

            for(int i = 0; i < num_rails; ++i)
            {
                for(int j = 0; j < real_lengths.get(i); ++j)
                {
                    buffer.append(rails.get(i).get(j));
                }
            }
        }
        return buffer.toString();
    }

    static String caesar(String msg, int rotate)
    {
        StringBuilder buffer = new StringBuilder();
        for(int i = 0; i < msg.length(); ++i)
        {
            int val = get_val(msg.charAt(i));
            if(val != -1)
            {
                buffer.append(get_char((val + rotate) % 25));
            }
            else
            {
                buffer.append(msg.charAt(i));
            }
        }
        return buffer.toString();
    }

    static String trans(String msg, String key)
    {
        ArrayList<ArrayList<Character>> cols = new ArrayList<>();
        ArrayList<Integer> vals = new ArrayList<>();

        for(int i = 0; i < key.length(); ++i)
        {
            ArrayList<Character> temp = new ArrayList<>();
            cols.add(temp);
            vals.add(get_val(key.charAt(i)));
        }

        for(int i = 0; i < msg.length(); ++i)
        {
            cols.get(i % key.length()).add(msg.charAt(i));
        }

        StringBuilder buffer = new StringBuilder();
        for(int i = 0; i < key.length(); ++i)
        {
            int low_val = 30;
            int low_index = -1;
            for(int j = 0; j < key.length(); ++j)
            {
                if(vals.get(j) < low_val)
                {
                    low_val = vals.get(j);
                    low_index = j;
                }
            }
            for(int j = 0; j < cols.get(low_index).size(); ++j)
            {
                buffer.append(cols.get(low_index).get(j));
            }
            vals.set(low_index, 29);
        }
        return buffer.toString();
    }

    static String four(String msg, String key1, String key2)
    {
        int index = 0;
        Set<Integer> grid1set = new HashSet<>();
        ArrayList<ArrayList<Integer>> grid1 = new ArrayList<>();
        for(int i = 0; i < 5; i++)
        {
            ArrayList<Integer> temp = new ArrayList<>();
            grid1.add(temp);
        }
        for(int i = 0; i < key1.length(); ++i)
        {
            if(!grid1set.contains(get_val(key1.charAt(i))))
            {
                grid1set.add(get_val(key1.charAt(i)));
                grid1.get(index/5).add(get_val(key1.charAt(i)));
                index += 1;
            }
        }
        for(int i = 0; i < 25; ++i)
        {
            if(!grid1set.contains(i))
            {
                grid1set.add(i);
                grid1.get(index/5).add(i);
                index += 1;
            }
        }

        index = 0;
        Set<Integer> grid2set = new HashSet<>();
        ArrayList<ArrayList<Integer>> grid2 = new ArrayList<>();
        for(int i = 0; i < 5; i++)
        {
            ArrayList<Integer> temp = new ArrayList<>();
            grid2.add(temp);
        }
        for(int i = 0; i < key2.length(); ++i)
        {
            if(!grid2set.contains(get_val(key2.charAt(i))))
            {
                grid2set.add(get_val(key2.charAt(i)));
                grid2.get(index/5).add(get_val(key2.charAt(i)));
                index += 1;
            }
        }
        for(int i = 0; i < 25; ++i)
        {
            if(!grid2set.contains(i))
            {
                grid2set.add(i);
                grid2.get(index/5).add(i);
                index += 1;
            }
        }

        int val1 = 0;
        int val2 = 0;
        StringBuilder buffer = new StringBuilder();
        for(int i = 0; i < msg.length()-1; i += 2)
        {
            val1 = get_val(msg.charAt(i))/5;
            val2 = get_val(msg.charAt(i+1))%5;
            buffer.append(get_char(grid1.get(val1).get(val2)));

            val1 = get_val(msg.charAt(i))%5;
            val2 = get_val(msg.charAt(i+1))/5;
            buffer.append(get_char(grid2.get(val1).get(val2)));
        }

        if(msg.length() % 2 == 1)
        {
            buffer.append(msg.charAt(msg.length() - 1));
        }

        return buffer.toString();
    }

    public static void main(String[] args)
    {
        Scanner input = new Scanner(System.in);
        int loops = Integer.parseInt(input.next());
        String msg;
        switch(Integer.parseInt(input.next()))
        {
            case 0:
                msg = input.next();
                int num_rails = Integer.parseInt(input.next());
                for(int i = 0; i < loops; ++i)
                {
                    System.out.print(rail_fence(msg, num_rails));
                }
                break;
            case 1:
                msg = input.next();
                int rotate = Integer.parseInt(input.next());
                for(int i = 0; i < loops; ++i)
                {
                    System.out.print(caesar(msg, rotate));
                }
                break;
            case 2:
                msg = input.next();
                String key = input.next();
                for(int i = 0; i < loops; ++i)
                {
                    System.out.print(trans(msg, key));
                }
                break;
            case 3:
                msg = input.next();
                String key1 = input.next();
                String key2 = input.next();
                for(int i = 0; i < loops; ++i)
                {
                    System.out.print(four(msg, key1, key2));
                }
                break;
        }
    }
}

