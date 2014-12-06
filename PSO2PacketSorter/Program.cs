using System;
using System.IO;
using System.Reflection;

namespace PSO2PacketSorter
{
    class Program
    {
        enum PacketType
        {
            None,
            Client,
            Server
        }

        static char seperator = Path.DirectorySeparatorChar;
        static string dirName = "_packets";
        static string currentDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        static int total = 0;
        static int current = 0;

        static void Main(string[] args)
        {
            Console.WriteLine("Sorting packets...");

            try
            {
                // Create the new sorted packet directory
                if (!Directory.Exists(dirName))
                    Directory.CreateDirectory(dirName);

                // Get the total number of files for later
                foreach (string directory in Directory.GetDirectories(currentDir))
                    foreach (string file in Directory.GetFiles(directory))
                        total++;

                // Iterate all the files and organize them
                Sort();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message + e.StackTrace + e.InnerException);
                return;
            }

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("Done!");

#if DEBUG
            Console.ReadLine();
#endif
        }

        static void Sort()
        {
            foreach (string directory in Directory.GetDirectories(currentDir))
            {
                // Skip the actual sorted folder
                if (directory.Contains(dirName))
                    continue;

                foreach (string file in Directory.GetFiles(directory))
                {
                    if (file.EndsWith(".bin")) // It should end in a bin file so we don't catch unnecessary files
                    {
                        DateTime time = File.GetLastWriteTime(file);
                        string timeString = string.Empty;
                        string newFile = string.Empty;
                        string type = string.Empty;
                        string name = string.Empty;
                        PacketType packetType = PacketType.None;

                        // We have a few different naming conventions, let's try and cover all of them
                        if (Path.GetFileName(file).Contains("-"))
                            type = Path.GetFileName(file).Split('.')[1].ToUpper();
                        else
                        {
                            string[] split = Path.GetFileName(file).Split('.');
                            type = (split[1] + "-" + split[2]).ToUpper();

                            // Polaris appends C and S to denote client versus server packets
                            if (split[3] == "S")
                                packetType = PacketType.Client;
                            else if (split[3] == "C")
                                packetType = PacketType.Server;
                        }

                        // Check to see if we have a folder for this type already
                        if (!Directory.Exists(currentDir + seperator + dirName + seperator + type))
                            Directory.CreateDirectory(currentDir + seperator + dirName + seperator + type);

                        // Time format strings
                        timeString = time.ToString("MM-dd-yy.HH-mm-ss.fff");

                        // Get the new name
                        switch (packetType)
                        {
                            case PacketType.None:
                                name = string.Format("{0}.{1}", type, timeString) + ".bin";
                                break;
                            case PacketType.Client:
                                name = string.Format("{0}.C.{1}", type, timeString) + ".bin";
                                break;
                            case PacketType.Server:
                                name = string.Format("{0}.S.{1}", type, timeString) + ".bin";
                                break;
                            default:
                                throw new Exception("Unknown packet type");
                        }
                        newFile = currentDir + seperator + dirName + seperator + type + seperator + name;

                        // Progress
                        current++;
                        WriteProgress();

                        // Copy it
                        if (!File.Exists(newFile))
                            File.Copy(file, newFile);
                        else
                            continue;
                    }
                }
            }
        }

        static void WriteProgress()
        {
            int size = 50;
            float percent = ((float)current / (float)total) * 100f;
            float barSize = percent * ((float)size / 100f);

            Console.Write("[");
            for (int i = 0; i < barSize; i++)
                Console.Write("=");
            for (float i = barSize; i < size; i++)
                Console.Write(" ");
            Console.Write("] {0:0.00}% {1,8} / {2}\r", percent, current, total);
        }
    }
}
