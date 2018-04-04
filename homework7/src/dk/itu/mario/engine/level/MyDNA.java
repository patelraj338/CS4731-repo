package dk.itu.mario.engine.level;

import com.sun.tools.javac.util.ArrayUtils;

import java.util.Random;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()


public class MyDNA extends DNA
{
	
	public int numGenes = 0; //number of genes

	// Return a new DNA that differs from this one in a small way.
	// Do not change this DNA by side effect; copy it, change the copy, and return the copy.
	public MyDNA mutate ()
	{
		MyDNA copy = new MyDNA();
		//YOUR CODE GOES BELOW HERE
		String currentString = this.getChromosome();
		int randIndex = ThreadLocalRandom.current().nextInt(0, currentString.length());

		char[] types = {'b', 'c', 'j', 'p', 'e'};
		int randCharIndex = ThreadLocalRandom.current().nextInt(0, 5);
		char randChar = types[randCharIndex];
		if (randChar == currentString.charAt(randIndex)) {
			randChar = types[(randCharIndex + 1) % 5];
		}

		StringBuilder stringer = new StringBuilder(currentString);
		stringer.setCharAt(randIndex, randChar);

		copy.setChromosome(stringer.toString());

		//YOUR CODE GOES ABOVE HERE
		return copy;
	}
	
	// Do not change this DNA by side effect
	public ArrayList<MyDNA> crossover (MyDNA mate)
	{
		ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
		//YOUR CODE GOES BELOW HERE
		int aLength = this.getChromosome().length() / 2;
		String aChromosome = this.getChromosome().substring(0, aLength);
		int bLength = mate.getChromosome().length() - aLength;
		String bChromosome = mate.getChromosome().substring(aLength, bLength);

		MyDNA newDNA = new MyDNA();
		newDNA.setChromosome(aChromosome.concat(bChromosome));
		offspring.add(newDNA);
		MyDNA newDNA2 = new MyDNA();
		newDNA2.setChromosome(bChromosome.concat(aChromosome));
		offspring.add(newDNA2);
		//YOUR CODE GOES ABOVE HERE
		return offspring;
	}
	
	// Optional, modify this function if you use a means of calculating fitness other than using the fitness member variable.
	// Return 0 if this object has the same fitness as other.
	// Return -1 if this object has lower fitness than other.
	// Return +1 if this objet has greater fitness than other.
	public int compareTo(MyDNA other)
	{
		int result = super.compareTo(other);
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return result;
	}
	
	
	// For debugging purposes (optional)
	public String toString ()
	{
		String s = super.toString();
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return s;
	}
	
	public void setNumGenes (int n)
	{
		this.numGenes = n;
	}

}

