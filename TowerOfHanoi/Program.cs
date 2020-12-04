using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace Hanoi
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("하노이 탑 디스크의 갯수를 입력하세요.(양의 정수)");

            int Discs = int.Parse(Console.ReadLine());

            while (TowerOfHanoi.GetNumberOfSteps(Discs) == -1)
            {
                Console.WriteLine("잘못된 양식입니다.");
                Console.Write("하노이 탑 디스크의 갯수를 입력하세요.(양의 정수)");
                Discs = int.Parse(Console.ReadLine());
            }

            var snapshots = TowerOfHanoi.SolveTowerOfHanoi(Discs);

            printSnapshots(snapshots);

            Console.WriteLine("----------------------------------------------------\n\n총 이동횟수 :" + TowerOfHanoi.GetNumberOfSteps(Discs));
        }

        private static void printSnapshots(List<List<int>[]> snapshots)
        {
            for (int i = 0; i < snapshots.Count; i++)
            {
                if (i == 0)
                {
                    Console.WriteLine($"Initial State --------------------------------------");
                }
                else
                {
                    Console.WriteLine($"Step {i}. --------------------------------------");
                }

                Console.WriteLine($"Start: [ {string.Join(", ", snapshots[i][0])} ]");
                Console.WriteLine($"Aux: [ {string.Join(", ", snapshots[i][1])} ]");
                Console.WriteLine($"End: [ {string.Join(", ", snapshots[i][2])} ]");
            }
        }

        private static bool isEqual(List<int> actual, List<int> expected)
        {
            if (actual.Count != expected.Count)
            {
                return false;
            }

            for (int i = 0; i < actual.Count; i++)
            {
                if (actual[i] != expected[i])
                {
                    return false;
                }
            }

            return true;
        }
    }
}
