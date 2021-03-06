#include "random_mapper.h"
#include "shim_mapper.h"

#include <cstdlib>
#include <map>

class RandomMapper : public ShimMapper
{
  public:
    RandomMapper(Machine, Runtime *, MapperRuntime *,
                 Processor, const char *name = NULL);
    virtual void select_task_options(Task*);
  private:
    std::map<Processor, Memory> all_sysmems;
    std::map<AddressSpaceID, std::set<Processor> > proc_map;
    AddressSpaceID num_nodes;
};

RandomMapper::RandomMapper(Machine machine, Runtime *rt, MapperRuntime *mrt,
                           Processor local_proc, const char *name /* = NULL */)
  : ShimMapper(machine, rt, mrt, local_proc, name),
    num_nodes(0)
{
  const std::set<Processor> &cpu_procs =
    machine_interface.filter_processors(Processor::LOC_PROC);

  for (std::set<Processor>::const_iterator it = cpu_procs.begin();
       it != cpu_procs.end(); ++it)
  {
    AddressSpaceID node_id = it->address_space();
    num_nodes = std::max(num_nodes, node_id + 1);
    proc_map[node_id].insert(*it);
    Memory sysmem =
      machine_interface.find_memory_kind(*it, Memory::SYSTEM_MEM);
    all_sysmems[*it] = sysmem;
  }
}

void RandomMapper::select_task_options(Task* task)
{
  task->inline_task = false;
  task->spawn_task = false;
  task->map_locally = true;
  task->profile_task = false;

  AddressSpaceID my_node_id = task->target_proc.address_space();
  AddressSpaceID next_node_id = my_node_id;
  while (num_nodes > 1 && my_node_id == next_node_id)
    next_node_id = (my_node_id + rand()) % num_nodes;

  Machine::ProcessorQuery procs = Machine::ProcessorQuery(machine).only_kind(Processor::LOC_PROC);
  std::vector<Processor> all_procs(procs.begin(), procs.end());

  task->target_proc =
    DefaultMapper::default_select_random_processor(
                                                   all_procs
                                                   // proc_map[next_node_id],
                                                   // Processor::LOC_PROC,
                                                   // machine
                                                   );
}

void register_random_mappers(Machine machine, HighLevelRuntime* rt,
                             const std::set<Processor>& local_procs)
{
  srand(12345);
  for (std::set<Processor>::const_iterator it = local_procs.begin();
        it != local_procs.end(); it++)
  {
    rt->replace_default_mapper(new RandomMapper(machine, rt, rt->get_mapper_runtime(), *it, "RandomMapper"), *it);
  }
}
