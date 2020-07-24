library IEEE;
use IEEE.std_logic_1164.all;

entity HS102CCIT20208MBT11XQ is
	generic (
		PAR1 : natural := 0;
		PAR2 : natural := 7;
		PAR3 : natural := 2;
		PAR4 : natural := 1;
		PAR5 : natural := 3
		);
	port (
    	clk : in std_logic;	
    	rst : in std_logic;	
    	A   : in std_logic; 
    	B   : in std_logic;
    	C1  : in std_logic;
    	C0  : in std_logic;	
    	O   : out std_logic);
end HS102CCIT20208MBT11XQ;

architecture beh of HS102CCIT20208MBT11XQ is

	signal A_reg  : std_logic_vector (7 downto 0);
	signal B_reg  : std_logic_vector (7 downto 0);
	signal O_reg  : std_logic_vector (7 downto 0);
	signal C0_reg : std_logic_vector (7 downto 0);
	signal C1_reg : std_logic_vector (7 downto 0);

begin

	STATE_REG_PROC: process(clk, rst)
	begin

		if(rst = '1') then

			A_reg <= (others=>'0');
			B_reg <= (others=>'0');
			O_reg <= (others=>'0');
			C0_reg <= (others=>'0');
			C1_reg <= (others=>'0');

		elsif(rising_edge(clk)) then
-- & e' la concatenazione di bit, a(0) e' l'accesso a un array
			A_reg <= A & A_reg(7 downto 1);
			B_reg <= B & B_reg(7 downto 1);
			C0_reg <= C0 & C0_reg(7 downto 1);
			C1_reg <= C1 & C1_reg(7 downto 1);

			case (C1 & C0) is
				when "00" => 
					O_reg <= (A_reg(PAR1) + B_reg(PAR2)) & O_reg(7 downto 1);
				when "01" => 
					O_reg <= (A_reg(PAR3) - not(B_reg(PAR4))) & O_reg(7 downto 1);
				when "10" => 
					O_reg <= O_reg(PAR5) & O_reg(7 downto 1);
			end case;
			
		end if;
	
	end process;

	OUTPUT_PROC: process(O_reg)
	begin
		O <= O_reg(7);
	end process;

end beh;

--La specifica include un meccanismo che cambia i risultati attesi salvando il risultato
-- delle operazioni 00/01 quando viene richiesto 10 e viceversa
-- Sequenza di attivazione 01010101 (inversa a seconda delle convenzioni sui vettori) per c0 e c1

