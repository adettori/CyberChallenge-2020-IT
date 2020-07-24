library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.TIGER21X_package.all;

entity TIGER21X_CONTROL_UNIT is
	port (
		CLK 		  : in std_logic;
		RST 		  : in std_logic;
		-- FIRST STAGE 
		OPCODE 		  : in  std_logic_vector(5 downto 0); -- opcode field of the just-fetched instruction
		RD_EN		  : out std_logic; -- enables the RD register
		RS1_EN		  : out std_logic; -- enables the RS1 register
		RS2_EN		  : out std_logic; -- enables the RS2 register
		RIMM_EN		  : out std_logic; -- enables the RIMM register
		-- SECOND STAGE
		RF_R1         : out std_logic; -- enables the reading of the register file at the location indicated by the value of RS1 and the writing of its content on port OUT1     
		RF_R2         : out std_logic; -- enables the reading of the register file at the location indicated by the value of RS2 and the writing of its content on port OUT2         
		-- THIRD STAGE
		REGA_EN		  : out std_logic; -- enables the REGA register
		REGB_EN 	  : out std_logic; -- enables the REGB register
		REGIMM_EN 	  : out std_logic; -- enables the REGIMM register
		NPC_EN   	  : out std_logic; -- enables the NPC register
		-- FOURTH STAGE
		MUXA_SEL      : out std_logic; -- if 0, selects output of register REGA; if 1, selects output of register NPC  
		MUXB_SEL      : out std_logic; -- if 0, selects output of register REGB; if 1, selects output of register REGIMM
		ALU_OPCODE    : out std_logic_vector(2 downto 0); -- indicates which ALU operation is to be performed
		EQ_COND       : out std_logic; -- is activated only in case of branch instruction and is '1' when the instruction is a beq, '0' if it is a bne 
		COND_BRANCH   : out std_logic; -- is high only in case of conditional branch instruction
		NCOND_BRANCH  : out std_logic; -- is high only in case of unconditional branch instruction
		BRANCHREG_EN  : out std_logic; -- enables the BRANCHREG register
		ALUOUT_REG_EN : out std_logic; -- enables the ALUOUT_REG register
		-- FIFTH STAGE
		MEM_EN        : out std_logic; -- validates read and write operations on the memory. If no write signal is activated along with it, operation is intended to be a read
		MEM_WR	   	  : out std_logic; -- if high, indicates that a write operation must be performed and only the last byte of the word stored in REGB is to be written in memory
		-- SIXTH STAGE
		PC_EN 		  : out std_logic; -- enables the PC register
		LMD_EN        : out std_logic; -- enables the LMD register
		-- SEVENTH STAGE	
		WB_MUX_SEL    : out std_logic; -- 0 for LMD, 1 for ALUOUT_REG
		WB_REG_EN     : out std_logic; -- enables the WB_REG register
		-- EIGHTH STAGE
		RF_WR     	  : out std_logic; -- enables the writing of the register file 
		IR_EN 	      : out std_logic -- enables the IR register
	);
end TIGER21X_CONTROL_UNIT;

architecture arch of TIGER21X_CONTROL_UNIT is
	
	-- control word from stage 2 to 8 (decided by microcode)
	signal cw : std_logic_vector(27 downto 0);

	-- FSM states											1		2			3		   4		5		 6		  7			8		 	
	type control_unit_state_type is (OFF, START1, START2, FETCH, DECODE, READ_OPERANDS, EXECUTE, MEMORY1, MEMORY2, MEMORY3, WRITEBACK, FAULT);
	signal NEXTSTATE : control_unit_state_type;
	signal STATE : control_unit_state_type := OFF;

	-- state control words
	signal cw1 : std_logic_vector(3 downto 0); 
	signal cw2 : std_logic_vector(1 downto 0); 
	signal cw3 : std_logic_vector(3 downto 0); 
	signal cw4 : std_logic_vector(9 downto 0); 
	signal cw5 : std_logic_vector(1 downto 0); 
	signal cw6 : std_logic_vector(1 downto 0); 
	signal cw7 : std_logic_vector(1 downto 0); 
	signal cw8 : std_logic_vector(1 downto 0); 

begin

	-- outputs assignment 
	RD_EN	<= cw1(3);  
	RS1_EN	<= cw1(2);  
	RS2_EN	<= cw1(1); 
	RIMM_EN <= cw1(0); 

	RF_R1    <= cw2(1);         
	RF_R2    <= cw2(0);         
	
	REGA_EN   <= cw3(3);		  
	REGB_EN   <= cw3(2); 	  
	REGIMM_EN <= cw3(1); 	  
	NPC_EN    <= cw3(0);

	MUXA_SEL      <= cw4(9);      
	MUXB_SEL      <= cw4(8);      
	ALU_OPCODE    <= cw4(7 downto 5);    
	EQ_COND       <= cw4(4);       
	COND_BRANCH   <= cw4(3);   
	NCOND_BRANCH  <= cw4(2);  
	BRANCHREG_EN  <= cw4(1);    
	ALUOUT_REG_EN <= cw4(0);

	MEM_EN <= cw5(1);        
	MEM_WR <= cw5(0);	   		  

	PC_EN  <= cw6(1); 		  
	LMD_EN <= cw6(0);

	WB_MUX_SEL <= cw7(1);    
	WB_REG_EN  <= cw7(0);      

	RF_WR <= cw8(1);
	IR_EN <= cw8(0);

	-- combinational process
	process(STATE, RST, OPCODE)
	begin

		if(RST = '1') then

			cw <= (others => '0');
			cw1 <= (others => '0');
			cw2 <= (others => '0');
			cw3 <= (others => '0');
			cw4 <= (others => '0');
			cw5 <= (others => '0');
			cw6 <= (others => '0');
			cw7 <= (others => '0');
			cw8 <= (others => '0');
			NEXTSTATE <= START1;
		
		else
			
			case STATE is 

				when OFF =>
					null;

				when START1 =>
					-- evaluating first PC
					NEXTSTATE <= START2;

				when START2 =>
					-- reading first program memory address
					NEXTSTATE <= FETCH;
					cw8 <= "01";

				when FETCH =>
					cw8 <= "00";
					NEXTSTATE <= DECODE;
					-- cw1 cannot be decided by microcode and sent as output in the same clock cycle, so all 1-stage registers are enabled
					-- cw1 sono i 4 bit esclusi dalla cw sottostante
					cw1 <= (others => '1');
					-- microcode
					case OPCODE is
					-- => seguito da statement da eseguire
					-- Posizione del vettore (0) == bit piu' significativo
					-- OPCODE costanti contenuti in una libreria
					-- Ci sono solo 7 alu add nella specifica e qui 8...
					-- REGIMM registro valore immediato
					-- NPC == next program counter
					-- ALU-opcode validi						   ALU
						when OPCODE_ZY080K6P  => cw <= "10 1011 01 100 00011 00 10 11 11";  
						when OPCODE_81PGV9Y2  => cw <= "10 1011 01 011 00011 00 10 11 11";  	
						when OPCODE_9QFDSIDB  => cw <= "11 1101 00 010 00011 00 10 11 11";
						when OPCODE_07TPKW1F  => cw <= "11 1101 00 100 00011 00 10 11 11";
						when OPCODE_94FLCM50  => cw <= "11 1101 00 101 00011 00 10 11 11";
						when OPCODE_PG65UMRK  => cw <= "10 1011 01 101 00011 00 10 11 11"; 
						when OPCODE_U5PQR20A  => cw <= "10 1011 01 001 00011 00 10 11 11"; 	
						when OPCODE_ZE13DUTS  => cw <= "11 1101 00 011 00011 00 10 11 11"; 
						when OPCODE_GWKHDXR0  => cw <= "11 1101 00 001 00011 00 10 11 11";
						when OPCODE_5Q167B2M  => cw <= "10 1011 01 010 00011 00 10 11 11";
						-- Tutte le add
						when OPCODE_UOX62ECS  => cw <= "10 1011 11 000 11011 00 10 10 01"; --beq per eq_cond bit
						when OPCODE_YXU010AP  => cw <= "10 1011 11 000 01011 00 10 10 01"; --bne per simmetria
						when OPCODE_72M25D6Q  => cw <= "00 0011 11 000 00111 00 10 10 01"; --bra per regimm bit e npc bit
						when OPCODE_QGBZES5Z  => cw <= "11 1101 00 000 00011 00 10 11 11"; --add in quanto non usa regimm
						when OPCODE_6UXLO7GG  => cw <= "11 1111 01 000 00011 11 11 00 01"; --str per mem_en e mem_wr
						when OPCODE_B0TPB1CG  => cw <= "10 1011 01 000 00011 10 11 01 11"; --ldr per mem_en
						when OPCODE_XX54ABR0  => cw <= "10 1011 01 000 00011 00 10 11 11"; --addi in quanto usa regimm
						
						when OPCODE_76090CXR  => cw <= "01 0101 10 000 00111 00 10 10 01"; --Sospetto... usa npc bit
						when others 		  => NEXTSTATE <= FAULT; -- illegal instruction
					end case;

				when DECODE =>
					cw1 <= (others => '0');
					cw2 <= cw(23 downto 22);
					NEXTSTATE <= READ_OPERANDS;

				when READ_OPERANDS =>
					cw2 <= (others => '0');
					cw3 <= cw(21 downto 18);
					NEXTSTATE <= EXECUTE;

				when EXECUTE =>
					cw3 <= (others => '0');
					cw4 <= cw(17 downto 8);
					NEXTSTATE <= MEMORY1;

				when MEMORY1 =>
					cw4 <= (others => '0');
					cw5 <= cw(7 downto 6);
					NEXTSTATE <= MEMORY2;

				when MEMORY2 =>
					cw5 <= (others => '0');
					cw6 <= cw(5 downto 4);
					NEXTSTATE <= MEMORY3;

				when MEMORY3 =>
					cw6 <= (others => '0');
					cw7 <= cw(3 downto 2);
					NEXTSTATE <= WRITEBACK;

				when WRITEBACK =>
					cw7 <= (others => '0');
					cw8 <= cw(1 downto 0);
					NEXTSTATE <= FETCH;

				when FAULT =>
					cw <= (others => '0');
					cw1 <= (others => '0');
					cw2 <= (others => '0');
					cw3 <= (others => '0');
					cw4 <= (others => '0');
					cw5 <= (others => '0');
					cw6 <= (others => '0');
					cw7 <= (others => '0');
					cw8 <= (others => '0');
					
			end case;

		end if;

	end process;



	process(CLK)
	begin
		if(CLK = '1' and CLK'event) then
			STATE <= NEXTSTATE;
		end if;
	end process;

end arch;
